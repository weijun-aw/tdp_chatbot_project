import random, json, torch, os
from googletrans import Translator, LANGUAGES
from ..algorithm.model import NeuralNet
from ..algorithm.nltk_utils import tokenize,stem,bag_of_words


def bryan_chatbot(sentence):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    file_name = 'intent.json'

    # Get the current directory of the script
    current_dir = os.path.dirname(__file__)

    # Create the full path to the JSON file
    file_path = os.path.join(current_dir, file_name)

    #Read json file
    with open(file_path,'r') as f:
        intent = json.load(f)

    #Open the model.pth file
    model_file = 'data.pth'
    model_file_path = os.path.join(current_dir, model_file)
    FILE = model_file_path
    # Create the full path to the JSON file


    #Load the data from the file
    data = torch.load(FILE)
    input_size = data["input_size"]
    hidden_size=data["hidden_size"]
    output_size = data["output_size"]
    all_words = data["all_words"]
    tags = data["tags"]
    model_state = data["model_state"]

    #Initialize the model
    model = NeuralNet(input_size,hidden_size,output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()

    #initialise the translator
    translator = Translator()

    bot_name="Jarvis"
    print("Let's chat! Type 'quit' to exit")
    while True:
        #sentence=input('You:')
        #if sentence.lower() =="quit":
        print(sentence)
        if sentence.lower() == "quit":
            break
        
        try:
            # Detect language

            detected_lang = translator.detect(sentence).lang
            # If not English, translate to English

            if detected_lang != 'en':
                sentence = translator.translate(sentence, src=detected_lang, dest='en').text
 
            # Tokenize the sentence the user input
            sentence = tokenize(sentence)
            # Convert the sentence to bag of words
            X = bag_of_words(sentence, all_words)
            # Reshape the bag of words
            X = X.reshape(1, X.shape[0])
            X = torch.from_numpy(X).to(device)

            # Pass the bag of words to the model
            output = model(X)
            # Get the index of the highest value
            _, predicted = torch.max(output, dim=1)
            tag = tags[predicted.item()]

            # Get the probability of the tag
            probs = torch.softmax(output, dim=1)
            prob = probs[0][predicted.item()]

            # Translate the response back to the original language if needed
            if prob.item() > 0.75:
                for intents in intent['intents']:
                    if tag == intents["tag"]:
                        response = random.choice(intents['responses'])
                        
                        # Translate response to the detected language
                        if detected_lang != 'en':
                            response = translator.translate(response, src='en', dest=detected_lang).text
                        
                        print(f"{bot_name}: {response}")
            else:
                response = "I am not trained to answer the question."
                
                # Translate response to the detected language
                if detected_lang != 'en':
                    response = translator.translate(response, src='en', dest=detected_lang).text
                
                print(f"{bot_name}: {response}")

        except Exception as e:
            print(f"An error occurred: {e}")

        return response