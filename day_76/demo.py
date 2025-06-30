#!/usr/bin/env python3
"""
FriendGPT Demo Script
Shows how to use the FriendGPT system programmatically
"""

from friendgpt import FriendGPT
import json

def demo_friendgpt():
    """Demonstrate FriendGPT features"""
    print("🤖 FriendGPT - Remember My People Demo")
    print("=" * 50)
    
    # Initialize FriendGPT
    fgpt = FriendGPT()
    
    # Add some sample friends
    print("\n📝 Adding sample friends...")
    
    friends_data = [
        {
            "name": "Akhil",
            "details": "Akhil, lives in Bangalore, loves cricket, just got a new job at TechCorp"
        },
        {
            "name": "Sarah",
            "details": "Sarah, works at Google, has 2 kids, enjoys hiking and photography"
        },
        {
            "name": "Mike",
            "details": "Mike, lives in New York, birthday March 15th, loves photography and coffee"
        },
        {
            "name": "Priya",
            "details": "Priya, lives in Mumbai, works as a doctor, loves cooking and travel"
        }
    ]
    
    for friend_info in friends_data:
        friend = fgpt.add_friend(friend_info["name"], friend_info["details"])
        print(f"✅ Added: {friend.name}")
        print(f"   Parsed details: {friend.details}")
    
    # Demonstrate conversation suggestions
    print("\n💬 Conversation Suggestions:")
    print("-" * 30)
    
    for friend_name in ["Akhil", "Sarah", "Mike", "Priya"]:
        print(f"\n🎯 Suggestions for {friend_name}:")
        suggestions = fgpt.get_conversation_suggestions(friend_name)
        for i, suggestion in enumerate(suggestions[:3], 1):
            print(f"   {i}. {suggestion}")
    
    # Demonstrate check-in messages
    print("\n📱 Generated Check-in Messages:")
    print("-" * 35)
    
    for friend_name in ["Akhil", "Sarah", "Mike", "Priya"]:
        message = fgpt.generate_checkin_message(friend_name)
        print(f"\n💌 {friend_name}:")
        print(f"   {message}")
    
    # Demonstrate conversation logging
    print("\n📚 Logging Sample Conversations:")
    print("-" * 35)
    
    sample_conversations = [
        ("Akhil", "Talked about his new job at TechCorp. He's excited about the role and learning new technologies. Mentioned he's settling well in Bangalore."),
        ("Sarah", "Caught up about her kids' school activities. She's planning a family hiking trip next month. Work at Google is going well."),
        ("Mike", "Discussed his photography projects. He's working on a coffee shop photo series. Birthday plans are coming together."),
        ("Priya", "Shared about her recent medical conference. Planning a cooking workshop. Travel plans for summer vacation.")
    ]
    
    for friend_name, conversation in sample_conversations:
        fgpt.log_conversation(friend_name, conversation)
        print(f"✅ Logged conversation with {friend_name}")
    
    # Show friends needing contact
    print("\n🕐 Friends Needing Contact:")
    print("-" * 25)
    
    friends_needing_contact = fgpt.get_friends_needing_contact(days_threshold=0)
    if friends_needing_contact:
        for friend_name in friends_needing_contact:
            print(f"   ⚠️ {friend_name} - needs contact")
    else:
        print("   ✅ All friends recently contacted")
    
    # Demonstrate search functionality
    print("\n🔍 Search Functionality:")
    print("-" * 20)
    
    search_terms = ["cricket", "Google", "photography", "doctor"]
    for term in search_terms:
        matches = fgpt.search_friends(term)
        print(f"   Search '{term}': {', '.join(matches) if matches else 'No matches'}")
    
    # Show final data structure
    print("\n📊 Final Data Structure:")
    print("-" * 25)
    
    for name, friend in fgpt.friends.items():
        print(f"\n👤 {name}:")
        print(f"   Location: {friend.details.get('location', 'Unknown')}")
        print(f"   Hobbies: {friend.details.get('hobbies', 'Unknown')}")
        print(f"   Work: {friend.details.get('work', friend.details.get('work_status', 'Unknown'))}")
        print(f"   Last Contact: {friend.last_contact}")
        print(f"   Conversations: {len(friend.conversation_history)}")
    
    print("\n🎉 Demo completed!")
    print("💡 Run 'python friendgpt.py' to use the full GUI interface")

def show_data_file():
    """Show the generated data file"""
    print("\n📄 Generated friends_data.json:")
    print("-" * 35)
    
    try:
        with open("friends_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            print(json.dumps(data, indent=2, ensure_ascii=False))
    except FileNotFoundError:
        print("No data file found. Run the demo first.")

if __name__ == "__main__":
    demo_friendgpt()
    show_data_file() 