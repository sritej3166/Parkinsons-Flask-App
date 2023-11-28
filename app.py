from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # Create an empty plot
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.02)

    for i in range(1, 4):
        fig.add_trace(go.Scatter(x=[], y=[], showlegend=False), row=i, col=1)

    # Set common x-axis and y-axis properties
    fig.update_xaxes(tickformat='%H:%M:%S.%L', showticklabels=True, row=3, col=1)
    fig.update_yaxes(title_text="Accelerometer X", row=1, col=1)
    fig.update_yaxes(title_text="Accelerometer Y", row=2, col=1)
    fig.update_yaxes(title_text="Accelerometer Z", row=3, col=1)

    # Update layout
    fig.update_layout(height=1000, hovermode='closest', dragmode='pan')

    # Convert the empty figure to JSON
    graphJSON = plotly.io.to_json(fig)

    # Render the template with the empty plot
    return render_template('index.html', graphJSON=graphJSON)


ALLOWED_VIDEO_EXTENSIONS = ['mp4']

def allowed_video_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS


@app.route('/', methods=['POST'])
def upload():    
    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return redirect(url_for('index'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            graphJSON = display_graph(filename)
            return render_template('index.html', graphJSON=graphJSON)

    elif 'video' in request.files:
        
        if 'video' not in request.files:
            return "No video found"
    
        video = request.files['video']

        if video.filename == "":
            return 'No video file selected'

        if video and allowed_video_file(video.filename):
            video.save('static/videos/' + video.filename)
            # Update the graphJSON and render the template
            graphJSON = display_graph('data.csv')
            return render_template('index.html', graphJSON=graphJSON, video_name=video.filename)

    return "Invalid file"


# @app.route('/', methods=['POST'])
# def u():
#     if 'file' not in request.files:
#         return redirect(url_for('index'))
#     file = request.files['file']
#     if file.filename == '':
#         return redirect(url_for('index'))
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)
#         graphJSON = display_graph(filename)
#         return render_template('index.html', graphJSON=graphJSON)
#         return redirect(url_for('display_graph', filename=filename))



# @app.route('/graph/<filename>')
def display_graph(filename):
    # Read the CSV data into a pandas 
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    df = pd.read_csv(file_path, parse_dates=['time'])

    # Create a figure with subplots
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.02)

    # Add traces for each subplot
    fig.add_trace(go.Scatter(x=df['time'], y=df['x_accel'], showlegend=False, hoverinfo='x+y', name='Accelerometer X'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['time'], y=df['y_accel'], showlegend=False, hoverinfo='x+y', name='Accelerometer Y'), row=2, col=1)
    fig.add_trace(go.Scatter(x=df['time'], y=df['z_accel'], showlegend=False, hoverinfo='x+y', name='Accelerometer Z'), row=3, col=1)

    fig.update_xaxes(tickformat='%H:%M:%S.%L',showticklabels=True, row=1, col=1)
    fig.update_xaxes(tickformat='%H:%M:%S.%L',showticklabels=True, row=2, col=1)
    fig.update_xaxes(tickformat='%H:%M:%S.%L',showticklabels=True, row=3, col=1)

    fig.update_xaxes(title_text="Timestamp", row=3, col=1)
    fig.update_yaxes(title_text="Accelerometer X", row=1, col=1)
    fig.update_yaxes(title_text="Accelerometer Y", row=2, col=1)
    fig.update_yaxes(title_text="Accelerometer Z", row=3, col=1)

    # Update layout to include the initial range
    fig.update_layout(
        height = 1000,
        yaxis=dict(fixedrange=True),
        yaxis2=dict(fixedrange=True),
        yaxis3=dict(fixedrange=True),
        hovermode='closest',
        dragmode='pan',
    )

    # Convert the figure to JSON
    graphJSON = plotly.io.to_json(fig)

    # Render the template with the plot
    return graphJSON


@app.route('/', methods=['POST'])
def u():
    if 'video' not in request.files:
        return "No video found"
    
    video = request.files['video']

    if video.filename == "":
        return 'No video file selected'
    
    if video and allowed_video_file(video.filename):
        video.save('static/videos/' + video.filename)
        return render_template('index.html', video_name=video.filename)

    
    return "Invalid video file"


if __name__ == '__main__':
    app.run(debug=True)
