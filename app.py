from flask import Flask, render_template, request, redirect, url_for
import boto3

app = Flask(__name__)

# AWS Configuration
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('FloodData')
sns_client = boto3.client('sns', region_name='us-east-1')
sns_topic_arn = 'arn:aws:sns:us-east-1:636529396572:FloodAlert' 

@app.route('/')
def index():
    try:
        response = table.scan()
        data = response['Items']
    except Exception as e:
        data = []
        print(f"Error fetching data: {e}")
    return render_template('index.html', data=data)

@app.route('/alert', methods=['POST'])
def send_alert():
    message = request.form['message']
    try:
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=message,
            Subject="Manual Flood Alert"
        )
        print("Alert sent successfully")
    except sns_client.exceptions.InvalidParameterException as e:
        print(f"Invalid parameter: {e}")
    except Exception as e:
        print(f"Error sending alert: {e}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
