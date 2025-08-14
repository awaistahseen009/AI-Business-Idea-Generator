from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models import BusinessIdea, User
from services.ai_workflow import BusinessIdeaWorkflow
import asyncio

ideas_bp = Blueprint('ideas', __name__)

def login_required(f):
    """Decorator to require login for routes"""
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@ideas_bp.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    user_email = session['user_email']
    # Derive a friendly display name from email (local part), e.g., john.doe -> John Doe
    local_part = user_email.split('@')[0] if user_email else ''
    display_name = ' '.join([part.capitalize() for part in local_part.replace('.', ' ').replace('_', ' ').split()]) or user_email
    
    # Get user's previous business ideas
    previous_ideas = BusinessIdea.get_by_user_id(user_id, limit=10)
    
    return render_template('dashboard.html', 
                         user_email=user_email,
                         display_name=display_name,
                         previous_ideas=previous_ideas)

@ideas_bp.route('/generate', methods=['GET', 'POST'])
@login_required
def generate():
    if request.method == 'POST':
        niche = request.form.get('niche', '').strip()
        web_search_enabled = request.form.get('web_search') == 'on'
        
        if not niche:
            flash('Please enter a niche or industry.', 'error')
            return render_template('ideas/generate.html')
        
        if len(niche) < 3:
            flash('Please enter a more specific niche (at least 3 characters).', 'error')
            return render_template('ideas/generate.html')
        
        try:
            # Initialize the AI workflow
            workflow = BusinessIdeaWorkflow()
            
            # Generate business ideas using the workflow
            result = workflow.run_workflow(niche, web_search_enabled)
            
            if result and 'ideas' in result:
                # Store the generated ideas in the database
                user_id = session['user_id']
                business_idea = BusinessIdea.create(
                    user_id=user_id,
                    niche=niche,
                    ideas=result['ideas'],
                    web_search_used=web_search_enabled
                )
                
                if business_idea:
                    flash('Business ideas generated successfully!', 'success')
                    return render_template('ideas/generate.html', 
                                         generated_ideas=result['ideas'],
                                         niche=niche,
                                         web_search_used=web_search_enabled,
                                         sources=result.get('sources', []))
                else:
                    flash('Ideas generated but failed to save to database.', 'warning')
                    return render_template('ideas/generate.html', 
                                         generated_ideas=result['ideas'],
                                         niche=niche,
                                         web_search_used=web_search_enabled,
                                         sources=result.get('sources', []))
            else:
                flash('Failed to generate business ideas. Please try again.', 'error')
                return render_template('ideas/generate.html')
                
        except Exception as e:
            print(f"Error generating ideas: {e}")
            flash('An error occurred while generating ideas. Please try again.', 'error')
            return render_template('ideas/generate.html')
    
    return render_template('ideas/generate.html')

@ideas_bp.route('/history')
@login_required
def history():
    user_id = session['user_id']
    user_email = session['user_email']
    
    # Get all user's business ideas with pagination
    page = request.args.get('page', 1, type=int)
    per_page = 5
    
    all_ideas = BusinessIdea.get_by_user_id(user_id, limit=50)  # Get more for pagination
    
    # Simple pagination
    start = (page - 1) * per_page
    end = start + per_page
    ideas_page = all_ideas[start:end]
    
    has_prev = page > 1
    has_next = len(all_ideas) > end
    
    return render_template('ideas/history.html',
                         user_email=user_email,
                         ideas=ideas_page,
                         page=page,
                         has_prev=has_prev,
                         has_next=has_next)

@ideas_bp.route('/view/<int:idea_id>')
@login_required
def view_idea(idea_id):
    user_id = session['user_id']
    
    # Get the specific business idea
    business_idea = BusinessIdea.get_by_id(idea_id)
    
    if not business_idea:
        flash('Business idea not found.', 'error')
        return redirect(url_for('ideas.history'))
    
    # Check if the idea belongs to the current user
    if business_idea.user_id != user_id:
        flash('You do not have permission to view this idea.', 'error')
        return redirect(url_for('ideas.history'))
    
    return render_template('ideas/view.html', business_idea=business_idea)
