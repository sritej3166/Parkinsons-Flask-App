from flask import Flask, render_template, request
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly

app = Flask(__name__,  static_folder='static')

@app.route('/')
def index():
    # Read the CSV data into a pandas DataFrame
    df = pd.read_csv('data.csv', parse_dates=['time'])

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
    return render_template('index.html', video_name=request.args.get('video_name'), graphJSON=graphJSON)

ALLOWED_EXTENSIONS = ['mp4']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return "No video found"
    
    video = request.files['video']

    if video.filename == "":
        return 'No video file selected'
    
    if video and allowed_file(video.filename):
        video.save('static/videos/' + video.filename)
        return render_template('index.html', video_name=video.filename)

    
    return "Invalid video file"

if __name__ == '__main__':
    app.run(debug=True)
