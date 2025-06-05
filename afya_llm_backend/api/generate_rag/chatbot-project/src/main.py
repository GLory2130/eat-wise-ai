from chatbot.bot import ChatBot

def main():
    chatbot = ChatBot()
    print("Welcome to the Chatbot! Type 'exit' to end the conversation.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        response = chatbot.get_response(user_input)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    main()