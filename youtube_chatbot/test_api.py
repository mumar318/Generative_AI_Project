"""
Test script for the YouTube Chatbot API
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_root():
    """Test root endpoint"""
    print("Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_load_video(video_id="VGFpV3Qj4as"):
    """Test loading a video"""
    print(f"Loading video: {video_id}...")
    response = requests.post(
        f"{BASE_URL}/load-video",
        json={"video_id": video_id}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    return response.json()

def test_chat(video_id, question, chat_history=None):
    """Test chat endpoint"""
    print(f"Asking: {question}...")
    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "video_id": video_id,
            "question": question,
            "chat_history": chat_history or []
        }
    )
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Answer: {result.get('answer', 'N/A')}\n")
    return result

def test_get_video_info(video_id):
    """Test get video info"""
    print(f"Getting info for video: {video_id}...")
    response = requests.get(f"{BASE_URL}/video/{video_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_cache_stats():
    """Test cache stats"""
    print("Getting cache stats...")
    response = requests.get(f"{BASE_URL}/cache/stats")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def main():
    """Run all tests"""
    print("=" * 60)
    print("YouTube Chatbot API Tests")
    print("=" * 60 + "\n")
    
    # Test root
    test_root()
    
    # Test load video
    video_id = "VGFpV3Qj4as"
    video_info = test_load_video(video_id)
    
    # Test get video info
    test_get_video_info(video_id)
    
    # Test cache stats
    test_cache_stats()
    
    # Test chat with conversation
    chat_history = []
    
    # First question
    result1 = test_chat(video_id, "What is this video about?")
    chat_history.append({
        "question": "What is this video about?",
        "answer": result1.get("answer", "")
    })
    
    # Follow-up question
    result2 = test_chat(video_id, "Can you tell me more about that?", chat_history)
    
    print("=" * 60)
    print("All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
