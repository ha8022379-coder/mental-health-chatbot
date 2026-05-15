from transformers import pipeline
import random

# Load AI emotion detection model
print("Loading AI emotion model...")
emotion_classifier = pipeline(
    'text-classification',
    model='j-hartmann/emotion-english-distilroberta-base',
    return_all_scores=False
)
print("AI emotion model loaded!")

# Map model emotions to our system emotions
emotion_map = {
    'joy': 'happy',
    'sadness': 'sad',
    'anger': 'angry',
    'fear': 'anxious',
    'disgust': 'hopeless',
    'surprise': 'neutral',
    'neutral': 'neutral'
}

def detect_emotion(text):
    text_lower = text.lower()

    # Keep keyword detection for crisis and greetings
    if any(word in text_lower for word in ['suicid', 'kill myself', 'end my life', 'want to die']):
        return "crisis"
    if any(word in text_lower for word in ['hi', 'hello', 'hey', 'howdy', 'greetings']):
        return "greeting"
    if any(word in text_lower for word in ['stress', 'stressed', 'overwhelmed', 'pressure']):
        return "stressed"
    if any(word in text_lower for word in ['lonely', 'alone', 'isolated', 'no one cares']):
        return "lonely"
    if any(word in text_lower for word in ['tired', 'exhausted', 'burnout', 'drained']):
        return "tired"
    if any(word in text_lower for word in ['grateful', 'thankful', 'blessed', 'peaceful']):
        return "grateful"

    # Use AI model for everything else
    try:
        result = emotion_classifier(text)[0]
        detected = result['label'].lower()
        return emotion_map.get(detected, 'neutral')
    except Exception as e:
        print(f"AI model error: {e}")
        return "neutral"

def get_response(emotion):
    responses = {
        "greeting": [
            "Hello! 👋 I'm so glad you're here. How are you feeling today?",
            "Hi there! 😊 Welcome. How are you doing today?",
            "Hey! 💙 I'm here to listen. How are you feeling right now?"
        ],
        "crisis": [
            "I'm very concerned about you right now 💙 Please reach out to a crisis helpline immediately. You are not alone and help is available. Please call 0311-7786264 (Pakistan) right now.",
            "What you're feeling is serious and I want you to get real help right now. Please contact a trusted person or call a helpline immediately. Your life matters ❤️"
        ],
        "anxious": [
            "I can feel that you're anxious right now 😔 Try taking 3 deep breaths slowly. Inhale for 4 seconds, hold for 4, exhale for 4. Would you like to talk about what's making you anxious?",
            "Anxiety can feel overwhelming but you are stronger than it 💙 What is worrying you the most right now?",
            "It's okay to feel anxious sometimes. You are not alone in this feeling. Can you tell me more about what's going on?"
        ],
        "angry": [
            "I understand you're feeling angry right now 😤 That's completely valid. Would you like to talk about what happened?",
            "Anger is a normal emotion. Take a moment to breathe and let it out safely. What's been frustrating you lately?",
            "It sounds like something really upset you. I'm here to listen without judgment. What's going on?"
        ],
        "lonely": [
            "Feeling lonely is one of the hardest feelings 💙 But remember, reaching out like this takes courage. I'm here with you right now.",
            "You are not as alone as you feel right now. I'm here and I care about how you're doing. Would you like to talk about it?",
        ],
        "stressed": [
            "Stress can feel like carrying the whole world 😔 Let's take it one step at a time. What's stressing you out the most right now?",
            "You're dealing with a lot it seems. Remember you don't have to solve everything at once. What's the biggest thing on your mind?",
        ],
        "tired": [
            "It sounds like you really need some rest 😴 Your body and mind are telling you something important. Are you getting enough sleep?",
            "Being exhausted affects everything. Please be kind to yourself today. What's been draining your energy?",
        ],
        "hopeless": [
            "I'm really sorry you're feeling this way 💙 Hopelessness is heavy but feelings do change. You reached out today and that matters a lot.",
            "Even in the darkest moments, things can get better. Would you like to talk about what's been happening?",
        ],
        "happy": [
            "That's wonderful to hear! 😊 I love that you're feeling good today! What's been making you happy?",
            "Your happiness is contagious! 🌟 Keep holding onto that feeling. What amazing thing happened today?",
        ],
        "sad": [
            "I'm sorry you're feeling sad 💙 It's okay to feel this way. Would you like to talk about what's making you sad?",
            "Sadness is hard to carry alone. I'm here to listen. What's been going on lately?",
        ],
        "grateful": [
            "That's beautiful 🌟 Gratitude is so powerful. What are you feeling grateful for today?",
            "It's wonderful that you're feeling this way! What's been good in your life lately?",
        ],
        "neutral": [
            "I'm here for you 😊 How has your day been going overall?",
            "Thanks for sharing. Would you like to talk about anything specific today?",
            "I'm listening. Is there anything on your mind you'd like to discuss?"
        ]
    }
    return random.choice(responses.get(emotion, responses["neutral"]))

# Test
if __name__ == "__main__":
    tests = [
        "I feel so happy today!",
        "I am very sad and crying",
        "I am so angry at everyone",
        "I feel scared and nervous",
        "I want to die",
        "hello",
        "I am grateful for everything"
    ]
    for test in tests:
        emotion = detect_emotion(test)
        print(f"Message: {test}")
        print(f"Emotion: {emotion}")
        print()