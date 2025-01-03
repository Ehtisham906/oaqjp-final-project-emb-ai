import requests

def emotion_detector(text_to_analyse):
    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    payload = {"raw_document": {"text": text_to_analyse}}

    try:
        # Send the API request
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Check for HTTP errors

        # Parse the API response
        response_dict = response.json()

        # Debug: Print the raw response
        print("API Response:", response_dict)

        # Extract emotion scores
        emotion_scores = response_dict.get('emotionPredictions', [{}])[0].get('emotion', {})
        if not emotion_scores:
            raise ValueError("Emotion scores not found in the response")

        # Determine dominant emotion
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)

        return {
            'anger': emotion_scores.get('anger', 0),
            'disgust': emotion_scores.get('disgust', 0),
            'fear': emotion_scores.get('fear', 0),
            'joy': emotion_scores.get('joy', 0),
            'sadness': emotion_scores.get('sadness', 0),
            'dominant_emotion': dominant_emotion
        }

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None
    except ValueError as ve:
        print(f"Error parsing response: {ve}")
        return None
