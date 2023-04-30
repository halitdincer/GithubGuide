from flask import Flask

app = Flask(__name__)

@app.route('/halitdincer/negate/tree/main/scripts')
def negate_scripts():
    return [
        "This code is a content script for a Chrome extension that detects and censors toxic text content in a webpage using a toxicity model. It retrieves the 'enable' setting from Chrome storage and, if enabled, creates a list of sentences, removes duplicates, filters short sentences, and classifies them with a toxicity model. Toxic sentences are wrapped in a 'censor' class. The script also adds a double-click event listener to toggle censoring on censored elements.",
        "The code is a minified version of jQuery v3.6.1, which is a popular, fast, and feature-rich JavaScript library. jQuery simplifies HTML document traversal, event handling, and animation, making it easy to work with HTML elements and their properties.",
        "This code snippet is for a Chrome extension's settings page, managing the 'enable' setting. It retrieves the 'checkbox_enable' element, gets the 'enable' value from Chrome storage, and sets the checkbox status. It also adds a 'change' event listener to update the 'enable' value in Chrome storage and logs the new status when the checkbox is toggled.",
        "The code is a minified version of the toxicity classifier, which is a JavaScript library for detecting toxic language in text. It is a part of the TensorFlow.js ecosystem and uses the Universal Sentence Encoder model to encode text into fixed-length embeddings.",
        "The code is a minified version of a library for use with TensorFlow.js. It contains utility functions, algorithms, and data structures for performing operations related to machine learning models, such as loading a pre-trained model, tokenizing and encoding text, and classifying input text based on the model's predictions."
    ]

@app.route('/halitdincer/negate/tree/main/styles')
def negate_styles():
    return [
        "This CSS file defines styles for a censored text and a bordered element. The censored text is black with a black background, and it changes to white text on a black background when hovered. The bordered element will have a 1px solid black border."
    ]

@app.route('/halitdincer/negate')
def negate():
    return [
        "This folder contains the script files for a Chrome extension that detects and censors toxic text on webpages using a toxicity model. It includes a content script, settings page, and necessary libraries such as jQuery, TensorFlow.js, and the toxicity classifier. The extension allows users to toggle censorship and manage the 'enable' setting for a seamless browsing experience.",
        "The folder contains a CSS file which applies styling to censored text and bordered elements. The censored text has a black background and text, revealing white text on hover. Bordered elements have a 1px solid black border.",
        "This folder contains various files for a web project, including a favicon, index.html, manifest.json, README, and subfolders for scripts and styles. The files and folders work together to create a functional, styled webpage with necessary resources and documentation.",
        "Negate is a browser extension designed to censor negative and toxic content on the internet, promoting mental well-being and a more welcoming online environment. Built using JavaScript and the co:here API, it identifies and censors toxic text content on webpages. Future plans include extending its capabilities to process media content like images, audio, and videos.",
        "A favicon.ico file is a small icon file used by web browsers to display a website's logo in the browser's address bar, tabs, and bookmarks.",
        "This HTML code is for the Negate browser extension's popup interface. It includes a title, a styled toggle switch, and a label to enable or disable the 'Block Negativity' feature. It also loads an external JavaScript file (popup.js) to handle the functionality of the toggle switch.",
        "The manifest file for the Negate browser extension provides essential details including its name, description, and version. It specifies icons, permissions, and the default popup and icon for the extension. It also lists the content security policy and content scripts, including CSS and JavaScript files, to be injected into webpages."
    ]
