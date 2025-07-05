"""
AI module for Smart Todo: Provides context analysis, task prioritization, categorization, and suggestions using NLP and ML techniques.
"""
import openai
import nltk
import re
import json
from datetime import datetime, timedelta
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from django.conf import settings

# Download required NLTK data if not already present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class SmartTaskAI:
    """
    Main AI class for Smart Todo. Handles context analysis, task prioritization, categorization, and suggestions.
    Uses OpenAI, NLTK, TextBlob, and scikit-learn for NLP and ML tasks.
    """
    def __init__(self):
        # Initialize OpenAI client if API key is set
        self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
        # TF-IDF vectorizer for keyword extraction
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        
    def analyze_context(self, context_data):
        """
        Analyze daily context for task-relevant information.
        Extracts keywords, sentiment, urgency, potential tasks, deadlines, people, and projects.
        """
        analysis = {
            'keywords': [],
            'sentiment_score': 0.0,
            'urgency_score': 0.0,
            'potential_tasks': [],
            'deadlines_mentioned': [],
            'people_mentioned': [],
            'projects_mentioned': []
        }
        
        if not context_data:
            return analysis
        
        # Extract text content
        text = context_data.get('content', '')
        
        # Sentiment analysis using TextBlob
        blob = TextBlob(text)
        analysis['sentiment_score'] = blob.sentiment.polarity
        
        # Urgency detection using keyword matching
        urgency_keywords = ['urgent', 'asap', 'immediately', 'deadline', 'due', 'emergency', 'critical']
        urgency_score = sum(1 for keyword in urgency_keywords if keyword.lower() in text.lower())
        analysis['urgency_score'] = min(urgency_score / len(urgency_keywords), 1.0)
        
        # Extract keywords using TF-IDF
        analysis['keywords'] = self._extract_keywords(text)
        
        # Find potential tasks using regex patterns
        analysis['potential_tasks'] = self._identify_potential_tasks(text)
        
        # Extract deadlines using regex
        analysis['deadlines_mentioned'] = self._extract_deadlines(text)
        
        # Extract people mentions using regex
        analysis['people_mentioned'] = self._extract_people(text)
        
        # Extract project mentions using regex
        analysis['projects_mentioned'] = self._extract_projects(text)
        
        return analysis
    
    def _extract_keywords(self, text):
        """
        Extract important keywords from text using TF-IDF.
        Returns a list of top keywords.
        """
        try:
            tfidf_matrix = self.vectorizer.fit_transform([text])
            feature_names = self.vectorizer.get_feature_names_out()
            tfidf_scores = tfidf_matrix.toarray()[0]
            
            # Get top 10 keywords by TF-IDF score
            keyword_indices = np.argsort(tfidf_scores)[-10:][::-1]
            keywords = [feature_names[i] for i in keyword_indices if tfidf_scores[i] > 0]
            
            return keywords
        except:
            return []
    
    def _identify_potential_tasks(self, text):
        """
        Identify potential tasks from context using regex patterns.
        Returns a list of up to 5 task strings.
        """
        task_patterns = [
            r'need to (.+?)(?:\.|$)',
            r'should (.+?)(?:\.|$)',
            r'have to (.+?)(?:\.|$)',
            r'must (.+?)(?:\.|$)',
            r'remember to (.+?)(?:\.|$)',
            r'don\'t forget to (.+?)(?:\.|$)',
            r'action item:? (.+?)(?:\.|$)',
            r'todo:? (.+?)(?:\.|$)',
            r'task:? (.+?)(?:\.|$)',
        ]
        
        potential_tasks = []
        for pattern in task_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            potential_tasks.extend(matches)
        
        return potential_tasks[:5]  # Return top 5 potential tasks
    
    def _extract_deadlines(self, text):
        """
        Extract deadline information from text using regex patterns.
        Returns a list of up to 3 deadline strings.
        """
        deadline_patterns = [
            r'due (.+?)(?:\.|$)',
            r'deadline (.+?)(?:\.|$)',
            r'by (.+?)(?:\.|$)',
            r'before (.+?)(?:\.|$)',
            r'until (.+?)(?:\.|$)',
        ]
        
        deadlines = []
        for pattern in deadline_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            deadlines.extend(matches)
        
        return deadlines[:3]
    
    def _extract_people(self, text):
        """
        Extract people mentions from text using regex patterns.
        Returns a list of up to 5 unique names or mentions.
        """
        people_patterns = [
            r'@(\w+)',  # @mentions
            r'from (\w+)',
            r'with (\w+)',
            r'contact (\w+)',
        ]
        
        people = []
        for pattern in people_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            people.extend(matches)
        
        return list(set(people))[:5]
    
    def _extract_projects(self, text):
        """
        Extract project mentions from text using regex patterns.
        Returns a list of up to 3 unique project names.
        """
        project_patterns = [
            r'project (\w+)',
            r'(\w+) project',
            r'#(\w+)',  # hashtag projects
        ]
        
        projects = []
        for pattern in project_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            projects.extend(matches)
        
        return list(set(projects))[:3]
    
    def prioritize_tasks(self, tasks, context_data=None):
        """
        AI-powered task prioritization based on task data and optional context.
        Returns a sorted list of tasks with AI priority scores and reasoning.
        """
        if not tasks:
            return []
        
        prioritized_tasks = []
        
        for task in tasks:
            priority_score = self._calculate_priority_score(task, context_data)
            task_data = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'current_priority': task.priority,
                'ai_priority_score': priority_score,
                'suggested_priority': self._score_to_priority(priority_score),
                'reasoning': self._generate_priority_reasoning(task, priority_score, context_data)
            }
            prioritized_tasks.append(task_data)
        
        # Sort by priority score (descending)
        prioritized_tasks.sort(key=lambda x: x['ai_priority_score'], reverse=True)
        
        return prioritized_tasks
    
    def _calculate_priority_score(self, task, context_data=None):
        """
        Calculate AI priority score for a task based on priority, deadline, and context.
        Returns a float score between 0 and 1.
        """
        score = 0.0
        
        # Base priority scoring
        priority_scores = {'low': 0.2, 'medium': 0.5, 'high': 0.8, 'urgent': 1.0}
        score += priority_scores.get(task.priority, 0.5) * 0.3
        
        # Deadline proximity scoring
        if task.deadline:
            days_until = (task.deadline - datetime.now()).days
            if days_until <= 1:
                score += 0.4
            elif days_until <= 3:
                score += 0.3
            elif days_until <= 7:
                score += 0.2
            else:
                score += 0.1
        
        # Context relevance
        if context_data:
            context_score = self._calculate_context_relevance(task, context_data)
            score += context_score * 0.3
        
        return min(score, 1.0)
    
    def _calculate_context_relevance(self, task, context_data):
        """Calculate how relevant the task is to current context"""
        if not context_data:
            return 0.0
        
        relevance_score = 0.0
        
        # Check for keyword overlap
        task_text = f"{task.title} {task.description}".lower()
        context_text = context_data.get('content', '').lower()
        
        # Simple keyword matching
        task_keywords = set(task_text.split())
        context_keywords = set(context_text.split())
        
        overlap = len(task_keywords.intersection(context_keywords))
        if overlap > 0:
            relevance_score += min(overlap / len(task_keywords), 0.5)
        
        # Check for urgency indicators in context
        if context_data.get('urgency_score', 0) > 0.5:
            relevance_score += 0.3
        
        return min(relevance_score, 1.0)
    
    def _score_to_priority(self, score):
        """Convert numerical score to priority level"""
        if score >= 0.8:
            return 'urgent'
        elif score >= 0.6:
            return 'high'
        elif score >= 0.4:
            return 'medium'
        else:
            return 'low'
    
    def _generate_priority_reasoning(self, task, score, context_data):
        """Generate reasoning for priority assignment"""
        reasons = []
        
        if task.deadline:
            days_until = (task.deadline - datetime.now()).days
            if days_until <= 1:
                reasons.append("Deadline is very close (within 1 day)")
            elif days_until <= 3:
                reasons.append("Deadline approaching (within 3 days)")
        
        if context_data and context_data.get('urgency_score', 0) > 0.5:
            reasons.append("High urgency detected in recent context")
        
        if task.priority == 'urgent':
            reasons.append("Marked as urgent priority")
        
        if not reasons:
            reasons.append(f"AI confidence score: {score:.2f}")
        
        return "; ".join(reasons)
    
    def suggest_deadline(self, task_data, context_data=None):
        """Suggest realistic deadlines for tasks"""
        base_duration = task_data.get('estimated_duration', 60)  # Default 1 hour
        
        # Adjust based on task complexity
        complexity_score = self._assess_complexity(task_data)
        adjusted_duration = base_duration * (1 + complexity_score)
        
        # Consider current workload
        suggested_deadline = datetime.now() + timedelta(hours=adjusted_duration / 60)
        
        # Adjust for weekends
        if suggested_deadline.weekday() >= 5:  # Saturday or Sunday
            days_to_monday = 7 - suggested_deadline.weekday()
            suggested_deadline += timedelta(days=days_to_monday)
        
        return {
            'suggested_deadline': suggested_deadline,
            'confidence': 0.7,
            'reasoning': f"Based on estimated duration ({adjusted_duration:.0f} minutes) and complexity analysis"
        }
    
    def _assess_complexity(self, task_data):
        """Assess task complexity (0-1 scale)"""
        description = task_data.get('description', '')
        title = task_data.get('title', '')
        
        complexity_indicators = ['research', 'analysis', 'development', 'design', 'planning', 'coordination']
        
        text = f"{title} {description}".lower()
        complexity_score = sum(1 for indicator in complexity_indicators if indicator in text)
        
        return min(complexity_score / len(complexity_indicators), 1.0)
    
    def categorize_task(self, task_data, existing_categories=None):
        """Auto-suggest task categories"""
        title = task_data.get('title', '')
        description = task_data.get('description', '')
        text = f"{title} {description}".lower()
        
        # Predefined category mappings
        category_keywords = {
            'work': ['meeting', 'project', 'deadline', 'client', 'report', 'presentation'],
            'personal': ['family', 'health', 'exercise', 'hobby', 'personal'],
            'shopping': ['buy', 'purchase', 'shop', 'grocery', 'store'],
            'health': ['doctor', 'appointment', 'medicine', 'exercise', 'fitness'],
            'finance': ['payment', 'bill', 'bank', 'money', 'budget', 'tax'],
            'education': ['study', 'course', 'learn', 'book', 'exam', 'homework'],
            'travel': ['trip', 'vacation', 'flight', 'hotel', 'travel'],
            'home': ['clean', 'repair', 'maintenance', 'home', 'house'],
        }
        
        scores = {}
        for category, keywords in category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                scores[category] = score
        
        if scores:
            suggested_category = max(scores, key=scores.get)
            confidence = scores[suggested_category] / len(category_keywords[suggested_category])
        else:
            suggested_category = 'general'
            confidence = 0.1
        
        return {
            'suggested_category': suggested_category,
            'confidence': confidence,
            'alternatives': sorted(scores.keys(), key=scores.get, reverse=True)[:3]
        }
    
    def enhance_task_description(self, task_data, context_data=None):
        """Enhance task description with AI"""
        original_description = task_data.get('description', '')
        title = task_data.get('title', '')
        
        if not original_description:
            # Generate description from title
            enhanced_description = f"Task: {title}\n\nSuggested steps:\n1. Plan the approach\n2. Execute the task\n3. Review and finalize"
        else:
            enhanced_description = original_description
        
        # Add context-based enhancements
        if context_data:
            relevant_context = self._extract_relevant_context(task_data, context_data)
            if relevant_context:
                enhanced_description += f"\n\nContext notes:\n{relevant_context}"
        
        return {
            'enhanced_description': enhanced_description,
            'confidence': 0.6,
            'added_context': bool(context_data)
        }
    
    def _extract_relevant_context(self, task_data, context_data):
        """Extract relevant context for task enhancement"""
        if not context_data:
            return ""
        
        task_keywords = set(f"{task_data.get('title', '')} {task_data.get('description', '')}".lower().split())
        context_text = context_data.get('content', '')
        
        # Simple relevance check
        relevant_sentences = []
        for sentence in context_text.split('.'):
            sentence_words = set(sentence.lower().split())
            if task_keywords.intersection(sentence_words):
                relevant_sentences.append(sentence.strip())
        
        return '. '.join(relevant_sentences[:2])  # Return top 2 relevant sentences
    
    def generate_task_suggestions(self, context_data):
        """Generate task suggestions based on context"""
        if not context_data:
            return []
        
        suggestions = []
        
        # Analyze context for potential tasks
        analysis = self.analyze_context(context_data)
        
        for potential_task in analysis['potential_tasks']:
            if len(potential_task.strip()) > 5:  # Filter very short tasks
                suggestion = {
                    'title': potential_task.strip().capitalize(),
                    'description': f"Generated from context: {context_data.get('context_type', 'unknown')}",
                    'suggested_category': self.categorize_task({'title': potential_task})['suggested_category'],
                    'suggested_priority': 'medium',
                    'confidence_score': 0.7,
                    'context_id': context_data.get('id')
                }
                suggestions.append(suggestion)
        
        return suggestions[:5]  # Return top 5 suggestions

# Create a global instance
task_ai = SmartTaskAI()