import random
from datetime import datetime
from glob import glob
from os.path import isdir, isfile

import ollama
from gpt4all import GPT4All

from .utils import read_file, reformat_logs, unformat_logs

# Define exit conditions for all functions
exit_conditions = [
    "exit",
    "goodbye",
    "bye",
    "good bye",
    "see ya",
    "/q",
    "quit",
    "hasta la vista",
]

# Define waiting messages for all functions
waiting_messages = [
    "You sure? Ok then",
    "Working on it",
    "After my smoke break",
    "I'll get right on that",
    "Running the permutations",
    "Beep boop",
    "Getting response",
    "Hold your horses",
    "Hey! I'm working here",
    "Is that a bird? Is that a plane? No! It's your response",
    "I'll be back",
    "Thinking really hard",
    "Waiting for Hermes to return",
]

# Define split condition
new_query_text = "-" * 15


class HephAIstus:
    def __init__(self):
        """
        Creates a new HephAIstus object
        """
        self._reset_logs()
        self._get_hammers()

    def _reset_logs(self):
        """
        Resets the logs to empty
        """
        # Initialize logs
        self.logs = []
        self.logs_loc = None

    def _save_logs(self):
        """
        Saves the logs to a text file
        """
        # Try to reformat logs
        try:
            self.logs = reformat_logs(self.logs, new_query_text)
        except TypeError:
            pass

        # Get save location
        default_save_loc = (
            "{0}.txt".format(datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))
            if self.logs_loc is None
            else self.logs_loc
        )
        save_loc = input("Save location (default: '{0}'): ".format(default_save_loc))
        if len(save_loc) == 0:
            save_loc = default_save_loc
        if not save_loc.endswith(".txt"):
            save_loc += ".txt"

        # Write logs
        with open(save_loc, "w") as outfile:
            outfile.write("\n".join(self.logs))
            outfile.close()
            print("Saved logs to {0}".format(save_loc))

    def load_logs(self, file_name: str):
        """
        Loads logs to be used by ollama
        """
        # Open the log file
        with open(file_name, "r") as input_file:
            # Update logs
            self.logs = unformat_logs(input_file.read(), new_query_text)
            self.logs_loc = file_name

    def _query(self):
        """
        Get the query from the user
        :return:
        str: User's query
        """
        # Get user's query
        query = input("Query (/o for options): ").strip()

        # Handle options
        if query.lower() == "/o":
            print(
                "Options:\n{0}".format(
                    "\n".join(
                        [
                            "/o: Options",
                            "/q: Quit",
                            "/f <file name> <query>: Send file(s) to bot",
                            "/n: Save and clear log and start a new conversation",
                        ]
                    )
                )
            )
            return self._query()

        # Handle exit
        if query.lower() in exit_conditions:
            return "/q"

        # Handle file
        if query.lower().startswith("/f"):
            # Get file name and query components
            file_name = query.split(" ")[1]
            query = " ".join(query.split(" ")[2:])

            # Handle directory
            if isdir(file_name):
                # Ensure it is formatted correctly
                if not file_name.endswith("/"):
                    file_name += "/"
                # Get all files in that directory
                file_names = glob("{0}**".format(file_name), recursive=True)

                # Get file information
                files = []
                for file_name in file_names:
                    files.append("{0}:".format(file_name))
                    try:
                        files.append("'{0}'".format(read_file(file_name)))
                    except ValueError:
                        files.pop()

                # Update query
                query = "{0}\n{1}".format(query, "\n".join(files))
            # Handle file is not present
            elif not isfile(file_name):
                print("File ({0}) does not exist".format(file_name))
                return self._query()
            else:
                # Get file information and update query
                query = "{0}\n'{1}'".format(query, read_file(file_name))

        # Handle new conversation
        if query.lower() == "/n":
            if input("Save logs (Y/N)? ").lower() == "y":
                self._save_logs()
            self._reset_logs()
            return self._query()

        # Print status message
        print("{0}...".format(random.choice(waiting_messages)))
        return query

    def forge(self, model_version: str = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"):
        """
        AI query tool that can use a specific model using gpt4all.
        Models are stored in /Users/<USER NAME>/.cache/gpt4all

        :param model_version:
        str: The model to use in the query
        """
        # Initialize model
        try:
            print("Loading model ({0})".format(model_version), end="\r")
            model = GPT4All(model_version)
            print("Loaded model    {0}".format(" " * len(model_version)))
        except ValueError:
            print(
                "Model ('{0}') was not found, please provide a different model.".format(
                    model_version
                )
            )
        else:
            # Get user's query
            query = self._query()

            # Reset logs
            self._reset_logs()

            # Open up chat session
            with model.chat_session():
                # Check that user doesn't want to exit
                while query.lower() != "/q":
                    # Save user query
                    self.logs.append(
                        "{0}\nQuery: {1}\n{0}".format(new_query_text, query)
                    )

                    # Get response from model
                    response = model.generate(query, max_tokens=1024) + "\n"
                    self.logs.append(response)
                    print("{0}\n{1}".format(new_query_text, response))

                    # Get user's query
                    query = self._query()

            # Save logs
            if input("Save logs (Y/N)? ").lower() == "y":
                self._save_logs()

    def _get_hammers(self):
        """
        Get a list of available ollama models on your local machine
        """
        # Get all models
        models = ollama.list()

        # Save models
        self.hammers = [model.model.split(":")[0] for model in models.models]
        self.hammers.sort()

    def list_hammers(self):
        """
        List available ollama models on your local machine
        """
        # Print out available models
        print("Available models:")
        for model in self.hammers:
            print("\t{0}".format(model))

    def create_hammers(self, model_loc: str = None, delete_from: bool = True):
        """
        Create all custom ollama models found on models folder

        :param model_loc:
        str: Optional location for the models. If not set, then will create the custom models in `src/hephaistus/models`
        :param delete_from:
        bool: If True, deletes FROM models for custom models.
        """
        # Get model files
        if model_loc is None:
            model_files = glob(
                "{0}/models/Modelfile_*".format("/".join(__file__.split("/")[:-1]))
            )
        else:
            if isdir(model_loc):
                model_files = glob("{0}/Modelfile_*".format(model_loc))
            elif isfile(model_loc):
                model_files = glob(model_loc)
            else:
                raise ValueError(
                    "Model location is not a directory/file: '{0}'".format(model_loc)
                )

        # Initialize from models
        from_models = []

        # Run through each model file
        for model_file in model_files:
            # Get name for the model from the file name
            model_name = model_file.split("/")[-1].replace("Modelfile_", "")
            print("Creating {0}".format(model_name), end="\r")

            # Get information from Modelfile
            params = {}
            with open(model_file, "r+") as input_file:
                # Run through each line of file
                for line in input_file:
                    # Format line
                    line = line.strip()

                    # Get from
                    if line.startswith("FROM"):
                        params["from_"] = line.split(" ")[1]
                    # Get parameters
                    elif line.startswith("PARAMETER"):
                        key = line.split(" ")[1]
                        value = float(line.split(" ")[2])
                        if "parameters" not in params:
                            params["parameters"] = {key: value}
                        else:
                            params["parameters"][key] = value
                    # Get system
                    elif line.startswith("SYSTEM"):
                        # Get end of SYSTEM setup
                        lines = [line]
                        next_line = next(input_file).strip()
                        while not next_line.startswith('"""'):
                            lines.append(next_line)
                            next_line = next(input_file).strip()
                        params["system"] = "\n".join(lines)

            # Create model
            ollama.create(model=model_name, **params)
            print("Created {0} ".format(model_name))

            # Save from model to clean-up afterward
            if delete_from:
                from_models.append(params["from_"])

        # Delete from models
        for from_model in list(set(from_models)):
            ollama.delete(from_model)
            print("Deleted {0}".format(from_model))

        # Update hammer list
        self._get_hammers()

    def hammer(self, model_version: str = "devops_engineer"):
        """
        AI query tool that can use a specific model using ollama

        :param model_version:
        str: The model to use in the query
        """
        # Check that model is available
        if model_version not in self.hammers:
            print(
                "Model ('{0}') was not found, please provide a different model.".format(
                    model_version
                )
            )
            return

        # Get user's query
        query = self._query()

        # Get new logs or already loaded logs
        if self.logs_loc is None:
            self._reset_logs()
        else:
            self.load_logs(self.logs_loc)

        # Check that user doesn't want to exit
        while query.lower() != "/q":
            # Save user query
            self.logs.append({"role": "user", "content": query})

            # Get response from model
            response = ollama.chat(model=model_version, messages=self.logs)
            # Output response
            self.logs.append({"role": "assistant", "content": response.message.content})
            print("{0}\n{1}\n".format(new_query_text, response.message.content))

            # Get user's query
            query = self._query()

        # Save logs
        if input("Save logs (Y/N)? ").lower() == "y":
            self._save_logs()
