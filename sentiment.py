from textblob import TextBlob
import random

def detect_emotion(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    text_lower = text.lower()

    negative_words = ['not', 'never', "don't", 'no', 'im not', 'never']

    # Greeting detection
    if any(word in text_lower for word in ['hi', 'hello', 'hey', 'howdy', 'greetings']):
        return "greeting"

    # Keyword based detection (smarter!)
    elif any(word in text_lower for word in ['suicid', 'kill myself', 'end my life', 'want to die']):
        return "crisis"

    elif any(word in text_lower for word in ['anxious', 'anxiety', 'panic', 'nervous', 'scared', 'afraid']):
        return "anxious"

    elif any(word in text_lower for word in ['angry', 'furious', 'frustrated', 'mad', 'irritated']):
        return "angry"

    elif any(word in text_lower for word in ['lonely', 'alone', 'isolated', 'no one cares']):
        return "lonely"

    elif any(word in text_lower for word in ['stress', 'stressed', 'overwhelmed', 'pressure', 'burden']):
        return "stressed"

    elif any(word in text_lower for word in ['tired', 'exhausted', 'burnout', 'drained', 'fatigued']):
        return "tired"

    elif any(word in text_lower for word in ['hopeless', 'worthless', 'useless', 'failure', 'hate myself']):
        return "hopeless"

    elif any(word in text_lower for word in ['happy', 'great', 'amazing', 'wonderful', 'excited', 'fantastic', 'won', 'winning', 'win', 'earned', 'got money', 'prize', 'good news', 'promoted', 'passed', 'success', 'achieved', 'celebrating', 'celebrate', 'awesome', 'brilliant', 'excellent', 'superb', 'delighted', 'thrilled', 'overjoyed']):
        if any(neg in text_lower for neg in negative_words):
            return "sad"
        return "happy"

    elif any(word in text_lower for word in ['sad', 'unhappy', 'depressed', 'miserable', 'cry', 'crying']):
        if any(neg in text_lower for neg in negative_words):
            return "happy"
        return "sad"

    elif any(word in text_lower for word in ['grateful', 'thankful', 'blessed', 'content', 'peaceful']):
        return "grateful"

    # Polarity based detection as backup
    if polarity > 0.3:
        return "happy"
    elif polarity > 0:
        return "neutral"
    elif polarity > -0.3:
        return "sad"
    else:
        return "hopeless"


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
            "Anxiety can feel overwhelming but you are stronger than it 💙 What is worrying you the most right now? Sometimes talking about it helps.",
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
            "Loneliness can be really painful. Thank you for sharing that with me. What's been making you feel this way?"
        ],
        "stressed": [
            "Stress can feel like carrying the whole world 😔 Let's take it one step at a time. What's stressing you out the most right now?",
            "You're dealing with a lot it seems. Remember you don't have to solve everything at once. What's the biggest thing on your mind?",
            "I hear you. Stress is exhausting. Have you been able to take any breaks for yourself lately?"
        ],
        "tired": [
            "It sounds like you really need some rest 😴 Your body and mind are telling you something important. Are you getting enough sleep?",
            "Being exhausted affects everything. Please be kind to yourself today. What's been draining your energy?",
            "Sometimes tiredness goes deeper than just sleep. How long have you been feeling this way?"
        ],
        "hopeless": [
            "I'm really sorry you're feeling this way 💙 Hopelessness is heavy but feelings do change. You reached out today and that matters a lot.",
            "Even in the darkest moments, things can get better. I know it's hard to believe that right now. Would you like to talk about what's been happening?",
            "You matter more than you know right now. Please don't give up. What's been making you feel hopeless?"
        ],
        "happy": [
            "That's wonderful to hear! 😊 I love that you're feeling good today! What's been making you happy?",
            "Your happiness is contagious! 🌟 Keep holding onto that feeling. What amazing thing happened today?",
            "So glad you're feeling great! 😄 You deserve all the happiness. Tell me more about your day!"
        ],
        "sad": [
            "I'm sorry you're feeling sad 💙 It's okay to feel this way. Would you like to talk about what's making you sad?",
            "Sadness is hard to carry alone. I'm here to listen. What's been going on lately?",
            "Your feelings are completely valid. I'm here with you. Can you tell me more about how you're feeling?"
        ],
        "grateful": [
            "That's beautiful 🌟 Gratitude is so powerful. What are you feeling grateful for today?",
            "It's wonderful that you're feeling this way! Cherish these moments. What's been good in your life lately?",
            "Gratitude can really change our perspective 😊 I love hearing this. Tell me more!"
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
        "hi",
        "hello",
        "im not happy",
        "im not sad",
        "I feel so anxious about my exams",
        "I am very happy today!",
        "I feel completely alone and no one cares",
        "I am so stressed with work",
        "I want to die"
    ]
    for test in tests:
        emotion = detect_emotion(test)
        response = get_response(emotion)
        print(f"\nMessage: {test}")
        print(f"Emotion: {emotion}")
        print(f"Response: {response}")