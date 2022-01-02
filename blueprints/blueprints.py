from flask import Blueprint


index_bp = Blueprint('index_bp',
                     __name__,
                     template_folder='index/templates',
                     static_folder='index/static')


users_bp = Blueprint('users_bp',
                    __name__,
                    template_folder='users/templates',
                    static_folder='users/static',
                    url_prefix='/users')


news_bp = Blueprint('news_bp',
                    __name__,
                    static_folder='news/static',
                    template_folder='news/templates',
                    url_prefix='/news')

games_bp = Blueprint('games_bp',
                     __name__,
                     url_prefix='/games',
                     static_folder='games/static',
                     template_folder='games/templates')


forum_bp = Blueprint('forum_bp',
                     __name__,
                     static_folder='forum/static',
                     template_folder='forum/templates',
                     url_prefix='/forum')

email_handler_bp = Blueprint('email_handler_bp',
                             __name__,
                             url_prefix='/emails',
                             template_folder='email_handler/templates')

message_bp = Blueprint('message_bp',
                       __name__,
                       static_folder='direct_messages/static',
                       template_folder='direct_messages/templates',
                       url_prefix='/messages')

authenticate_bp = Blueprint('authenticate_bp',
                            __name__,
                            url_prefix='/authenticate',
                            template_folder='authenticate_handler/templates')