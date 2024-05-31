from flask import Flask, redirect,  url_for, render_template
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image, ImageEnhance, ImageFilter
from tkinter import filedialog
import os

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")

    