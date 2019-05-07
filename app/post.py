import os
from flask import Blueprint, flash, redirect, url_for,request
from flask_login import login_required, current_user
from flask import render_template
from flask import send_from_directory
from werkzeug.utils import secure_filename
from app import app, db
from app.forms import CreatePost ,CommentForm
from app.models import Post , Comment, User, Tag
bp = Blueprint('post', __name__, url_prefix='/post')





@app.route('/uploads/<filename>')
def uploaded_file(filename):
  return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@bp.route('/')
def index():
	page = request.args.get('page', 1, type=int)
	posts = db.session.query(Post, User).filter(User.id == Post.user_id).add_columns(Post.id, Post.image_path, Post.title, Post.title, Post.body, Post.like, Post.dislike, Post.timestamp, User.username).order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
	if posts.has_next:
		next_url = url_for('post.index', page=posts.next_num) 
	else:
		next_url = None	

	if posts.has_prev:
		prev_url = url_for('post.index', page=posts.prev_num) 
	else:
		prev_url = None
	return render_template('post/index.html', title='Home', posts=posts.items, next_url=next_url, prev_url=prev_url)

@bp.route('/tags')
def tags_index():
	tags = Tag.query.all()
	return render_template('post/tags_index.html', title='Home', tags=tags)

@bp.route('/search_post', methods=['GET', 'POST'])
def search_post():
	if request.method=='POST':
		results = []
		search_results = request.form['body']
		page = request.args.get('page', 1, type=int)
		if search_results == '':
			posts = db.session.query(Post, User).filter(User.id == Post.user_id).add_columns(Post.id, Post.image_path, Post.title, Post.title, Post.body, Post.like, Post.dislike, Post.timestamp, User.username).order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
		if len(search_results) > 0:
			posts = db.session.query(Post, User).filter(Post.title == search_results).filter(User.id == Post.user_id).add_columns(Post.id, Post.image_path, Post.title, Post.title, Post.body, Post.like, Post.dislike, Post.timestamp, User.username).order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)

		if posts.has_next:
			next_url = url_for('post.index', page=posts.next_num) 
		else:
			next_url = None	
		if posts.has_prev:
			prev_url = url_for('post.index', page=posts.prev_num) 
		else:
			prev_url = None		

		if not posts:
			flash('No results found!')
			return redirect('/post')
		else:
			return render_template('post/index.html', title='Home', posts=posts.items, next_url=next_url, prev_url=prev_url)

@bp.route('/detail/<int:id>')
def detail(id):
	post = Post.query.get(id)
	try:
		comments = Comment.query.all() 
	except:
		comments = False
	users = User.query.all()
	return render_template('post/detail.html', title='Detail', post = post, comments = comments, users=users)


@bp.route('/tag_with_psot/<int:id>')
def tag_with_psot(id):
	tag = Tag.query.filter(Tag.id == id).first()
	posts = tag.posts
	return render_template('post/index.html', posts=posts)


@login_required
@bp.route('/comment/<int:id>', methods=['GET','POST'])
def add_comemnt(id):
	if request.method=='POST':
		body = request.form['body']
		com = Comment(body=body, user_id=current_user.get_id(), post_id=id)
		db.session.add(com)
		db.session.commit()
		return redirect(url_for('post.detail', id=id))

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_required
@bp.route('/create', methods=['GET','POST'])
def create():
	form = CreatePost()
	if form.validate_on_submit():

		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		
		post = Post(title = form.title.data, body=form.body.data, image_path = filename)
		user = User.query.get(current_user.get_id())
		user.posts.append(post)
		db.session.add(user)

		for tag in form.tags.data.split(' '):
			if Tag.query.filter(Tag.body == tag).first():
				add_tag = Tag.query.filter(Tag.body == tag).first()
				post.tags.append(add_tag)
			else:
				add_tag = Tag(body=tag)
				post.tags.append(add_tag)
				db.session.add(add_tag)
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('post.index'))
	return render_template('post/create.html', title='Create Post', form=form)


@login_required
@bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
	form = CreatePost()
	post = Post.query.get(id)
	if form.validate_on_submit():
		post.title = form.title.data
		post.body = form.body.data
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('post.index'))
	elif request.method == "GET":
		form.title.data = post.title
		form.body.data = post.body
	return render_template('post/update.html', title='Update Post', form = form, post=post )


@login_required
@bp.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
	post = Post.query.get(id)
	print()
	print(post)
	print()
	db.session.delete(post)
	db.session.commit()
	return redirect(url_for('post.index'))

@login_required
@bp.route('/like/<int:id>', methods=['GET','POST'])
def like(id):
	post = Post.query.get(id)
	post.like += 1
	db.session.commit()
	return redirect(url_for('post.detail', id=post.id))


@login_required
@bp.route('/dislike/<int:id>', methods=['GET','POST'])
def dislike(id):
	post = Post.query.get(id)
	post.dislike += 1
	db.session.commit()
	return redirect(url_for('post.detail', id=post.id))

