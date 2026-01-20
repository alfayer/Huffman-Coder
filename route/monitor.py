from flask import Blueprint, redirect, render_template

monitor_bp = Blueprint('monitor', __name__,url_prefix='/')

@monitor_bp.route('/monitor', methods=['GET'])
def monitor():
    redirect_url = "http://localhost:8000"
    redirect(redirect_url,code=301)
    