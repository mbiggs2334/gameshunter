from gamehunter import db
from datetime import datetime
from app import app
from flask import g
from blueprints.users.models import User, Follow
from blueprints.games.models import Games
from blueprints.forum.models import Post, Comment

db.drop_all()
db.create_all()

now = datetime.utcnow()

u1 = User.signup('digitortn', 'email1@email.com', 'nWbuGJX6ukNA')
u2 = User.signup('pretzelsblurt', 'email2@email.com', 'nWbuGJX6ukNA')
u3 = User.signup('crushbasil', 'email3@email.com', 'nWbuGJX6ukNA')
u4 = User.signup('frayoxygen', 'email4@email.com', 'nWbuGJX6ukNA')
u5 = User.signup('rinklard', 'email5@email.com', 'nWbuGJX6ukNA')
u6 = User.signup('sweatpantswren', 'email6@email.com', 'nWbuGJX6ukNA')
u7 = User.signup('limbicshark', 'email7@email.com', 'nWbuGJX6ukNA')
u8 = User.signup('chileanmustard', 'email8@email.com', 'nWbuGJX6ukNA')
u9 = User.signup('upholdceiling', 'email9@email.com', 'nWbuGJX6ukNA')
u10 = User.signup('rathercrystals', 'email10@email.com', 'nWbuGJX6ukNA')
u1.profile_image = True
u1.profile_image_uploaded = True
u1.email_confirmed = True
u1.last_active = now
u2.profile_image = True
u2.profile_image_uploaded = True
u2.email_confirmed = True
u2.last_active = now
u3.profile_image = True
u3.profile_image_uploaded = True
u3.email_confirmed = True
u3.last_active = now
u4.profile_image = True
u4.profile_image_uploaded = True
u4.email_confirmed = True
u4.last_active = now
u5.profile_image = True
u5.profile_image_uploaded = True
u5.email_confirmed = True
u5.last_active = now
u6.profile_image = True
u6.profile_image_uploaded = True
u6.email_confirmed = True
u6.last_active = now
u7.profile_image = True
u7.profile_image_uploaded = True
u7.email_confirmed = True
u7.last_active = now
u8.profile_image = True
u8.profile_image_uploaded = True
u8.email_confirmed = True
u8.last_active = now
u9.profile_image = True
u9.profile_image_uploaded = True
u9.email_confirmed = True
u9.last_active = now
u10.profile_image = True
u10.profile_image_uploaded = True
u10.email_confirmed = True
u10.last_active = now
db.session.add(u1)
db.session.add(u2)
db.session.add(u3)
db.session.add(u4)
db.session.add(u5)
db.session.add(u6)
db.session.add(u7)
db.session.add(u8)
db.session.add(u9)
db.session.add(u10)
db.session.commit()

Games.create_new_game(rawg_id=3070,
                      title='Fallout 4',
                      background_img='https://media.rawg.io/media/games/d82/d82990b9c67ba0d2d09d4e6fa88885a7.jpg',
                      release_date='2015-11-09')

Games.create_new_game(rawg_id=4535,
                      title='Call of Duty 4: Modern Warfare',
                      background_img='https://media.rawg.io/media/games/9fb/9fbaea2168caea1f806546dfdaaeb1da.jpg',
                      release_date='2007-11-05')

Games.create_new_game(rawg_id=375231,
                      title='Mini Motorways',
                      background_img="https://media.rawg.io/media/screenshots/2d3/2d33aaeb43e5e520fb4b2e545e1662cf.jpg",
                      release_date='2021-07-20')

Games.create_new_game(rawg_id=2093,
                      title="No Man's Sky",
                      background_img="https://media.rawg.io/media/games/174/1743b3dd185bda4a7be349347d4064df.jpg",
                      release_date='2016-08-09')

Games.create_new_game(rawg_id=427930,
                      title='Phasmophobia',
                      background_img="https://media.rawg.io/media/screenshots/75c/75c9b2a8e308bb44059d52ff59006e16.jpg",
                      release_date='2020-09-18')

with app.app_context():
    g.user = u1
    
    Follow.create_new_follow(other_user=u2)
    Follow.create_new_follow(other_user=u4)
    Follow.create_new_follow(other_user=u8)
    Follow.create_new_follow(other_user=u10)
    
    p1 = Post.create_new_post(game_id=4535,
                         title='Aenean eleifend dui vitae mi mattis',
                         content='Sed varius in arcu vel vestibulum. Quisque finibus mi at ex convallis, sed accumsan ex euismod. Proin malesuada dui vel elit lobortis, nec finibus ipsum facilisis. Donec euismod nisl mauris, sit amet tempus tellus gravida sed. Phasellus nisi enim, consectetur eu sollicitudin et, pretium at arcu. Aliquam non nibh vel leo pharetra tempor. Duis pellentesque sed orci ut pharetra. Etiam vitae massa sed odio vulputate laoreet.')

    p2 = Post.create_new_post(game_id=427930,
                         title='Ut pellentesque tortor augue',
                         content='Cras iaculis interdum ligula at euismod. Donec enim mauris, ultricies ut tincidunt quis, condimentum nec ex. Proin eget ipsum ultricies, ultricies dolor et, finibus tellus. Vestibulum imperdiet consectetur erat, vitae imperdiet velit dictum quis. Sed eleifend massa sit amet elit pulvinar vehicula. Vestibulum in convallis massa. Vestibulum in lectus sapien. Aenean efficitur porttitor mauris vel congue.')

    p3 = Post.create_new_post(game_id=2093,
                         title='Vivamus sed lacus at lectus cursus tristique eget vel mauris',
                         content='Cras venenatis ullamcorper ornare. Interdum et malesuada fames ac ante ipsum primis in faucibus. Aliquam quis condimentum eros. Fusce dapibus libero at ligula pulvinar scelerisque. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis vehicula molestie felis id euismod. Nullam diam orci, mollis vitae massa eu, vestibulum vestibulum metus. Quisque bibendum, orci id vulputate mattis, tortor lectus commodo metus, ut hendrerit est lacus sit amet sapien.')

    g.user = u2
    Follow.create_new_follow(other_user=u1)
    Follow.create_new_follow(other_user=u5)
    Follow.create_new_follow(other_user=u7)
    Follow.create_new_follow(other_user=u9)
    
    p4 = Post.create_new_post(game_id=3070,
                         title='Curabitur arcu sapien, blandit eget malesuada at, interdum non arcu',
                         content='Donec ultrices porta purus eu venenatis. Vivamus ut ultrices odio. Praesent congue eget mi ut placerat. Praesent sit amet pulvinar elit. Aenean ex nisi, sollicitudin eu ultricies id, varius tristique turpis. Morbi mollis euismod dui. Quisque consectetur sapien metus, dignissim dictum augue vehicula in. Donec non malesuada orci, eu ornare nunc. Quisque tristique et tortor sit amet interdum. Phasellus ac metus arcu.')

    p5 = Post.create_new_post(game_id=4535,
                         title='Duis feugiat enim vel porttitor sodales',
                         content='Duis vitae vehicula tellus. Proin placerat non sapien vitae blandit. Aenean venenatis tortor id arcu mollis vestibulum. Fusce sed odio vitae leo placerat dapibus. Donec nec consectetur lacus, volutpat interdum nunc. Suspendisse lectus lectus, auctor vel leo eu, malesuada rhoncus dui. Duis felis tortor, vulputate ut porttitor id, accumsan vel justo. Mauris a tellus a erat lacinia vestibulum. Suspendisse luctus felis non nibh cursus rutrum. Sed tempus mauris ac consectetur consectetur.')

    
    g.user = u3
    Follow.create_new_follow(other_user=u1)
    Follow.create_new_follow(other_user=u2)
    Follow.create_new_follow(other_user=u4)
    Follow.create_new_follow(other_user=u6)
    Follow.create_new_follow(other_user=u7)
    Follow.create_new_follow(other_user=u10)
    
    p6 = Post.create_new_post(game_id=375231,
                         title='Fusce sed odio vitae leo placerat dapibus',
                         content='Donec nec consectetur lacus, volutpat interdum nunc. Suspendisse lectus lectus, auctor vel leo eu, malesuada rhoncus dui. Duis felis tortor, vulputate ut porttitor id, accumsan vel justo. Mauris a tellus a erat lacinia vestibulum. Suspendisse luctus felis non nibh cursus rutrum. Sed tempus mauris ac consectetur consectetur.')

    p7 = Post.create_new_post(game_id=2093,
                         title='In euismod, velit et iaculis sagittis',
                         content='Quisque condimentum tellus vitae dui finibus, vel ultrices dui scelerisque. Aliquam sed varius turpis. In pharetra pellentesque risus ac fermentum. In laoreet vitae enim ac ultrices. In id sem consectetur, elementum neque nec, aliquet ante. Donec et lobortis diam. Etiam eu est sodales, iaculis urna at, interdum odio. Aenean vitae maximus dui. Nulla facilisi. Sed sed tempor felis. Sed at suscipit elit.')

    
    g.user = u4
    Follow.create_new_follow(other_user=u1)
    Follow.create_new_follow(other_user=u2)
    Follow.create_new_follow(other_user=u6)
    
    p8 = Post.create_new_post(game_id=375231,
                         title='Mauris quis porta enim',
                         content='Curabitur mollis aliquam ante, vitae porta ipsum rutrum et. Vivamus rhoncus gravida turpis, non porttitor nunc porta et. Aliquam gravida iaculis turpis, eget rutrum lorem ullamcorper non. Cras arcu dolor, volutpat eu convallis ut, gravida sed ligula. Quisque tincidunt nisl ac sapien venenatis egestas. Phasellus ut sem et ante pharetra vestibulum ac quis enim. Nam porttitor vulputate mi, porttitor viverra tellus malesuada et.')

    p9 = Post.create_new_post(game_id=427930,
                         title='Fusce a lacinia augue, nec venenatis leo',
                         content='In lobortis congue justo, non malesuada diam ullamcorper sit amet. Cras libero quam, malesuada nec sem et, mattis sollicitudin augue. Nam volutpat felis vitae leo tempor, id mattis dui lobortis. Suspendisse sapien eros, feugiat vitae lacus eu, faucibus maximus urna. Nullam scelerisque convallis lorem. Maecenas volutpat iaculis felis pharetra rutrum. Cras molestie tincidunt erat sed molestie. Pellentesque vestibulum porttitor dolor, id semper est varius at.')
    
    g.user = u5
    Follow.create_new_follow(other_user=u4)
    Follow.create_new_follow(other_user=u7)
    Follow.create_new_follow(other_user=u9)
    
    p10 = Post.create_new_post(game_id=2093,
                         title='Fusce ullamcorper id leo et mollis',
                         content='Cras tellus erat, elementum vitae tellus ac, dapibus porta ligula. Pellentesque mollis orci id erat tristique, eget tincidunt lectus dictum. Cras hendrerit tincidunt arcu, nec eleifend urna. In arcu diam, mattis quis porta quis, placerat et odio. Ut sed urna hendrerit, lobortis lectus ut, volutpat orci.')
   
    p11 = Post.create_new_post(game_id=4535,
                         title='Mauris ac dolor lacinia ligula posuere aliquam',
                         content='Maecenas hendrerit volutpat libero. Donec condimentum sem quis lorem sodales, finibus sagittis turpis iaculis. Nulla at metus blandit, laoreet odio a, egestas leo. In lobortis congue justo, non malesuada diam ullamcorper sit amet. Cras libero quam, malesuada nec sem et, mattis sollicitudin augue.')
   

    g.user = u6
    Follow.create_new_follow(other_user=u2)
    Follow.create_new_follow(other_user=u3)
    Follow.create_new_follow(other_user=u5)
    Follow.create_new_follow(other_user=u8)
    Follow.create_new_follow(other_user=u10)
    
    p12 = Post.create_new_post(game_id=375231,
                         title='Aenean eleifend dui vitae mi mattis',
                         content='Sed varius in arcu vel vestibulum. Quisque finibus mi at ex convallis, sed accumsan ex euismod. Proin malesuada dui vel elit lobortis, nec finibus ipsum facilisis. Donec euismod nisl mauris, sit amet tempus tellus gravida sed. Phasellus nisi enim, consectetur eu sollicitudin et, pretium at arcu. Aliquam non nibh vel leo pharetra tempor. Duis pellentesque sed orci ut pharetra. Etiam vitae massa sed odio vulputate laoreet.')

    p13 = Post.create_new_post(game_id=3070,
                         title='Ut pellentesque tortor augue',
                         content='Cras iaculis interdum ligula at euismod. Donec enim mauris, ultricies ut tincidunt quis, condimentum nec ex. Proin eget ipsum ultricies, ultricies dolor et, finibus tellus. Vestibulum imperdiet consectetur erat, vitae imperdiet velit dictum quis. Sed eleifend massa sit amet elit pulvinar vehicula. Vestibulum in convallis massa. Vestibulum in lectus sapien. Aenean efficitur porttitor mauris vel congue.')
    
    p14 = Post.create_new_post(game_id=2093,
                         title='Vivamus sed lacus at lectus cursus tristique eget vel mauris',
                         content='Cras venenatis ullamcorper ornare. Interdum et malesuada fames ac ante ipsum primis in faucibus. Aliquam quis condimentum eros. Fusce dapibus libero at ligula pulvinar scelerisque. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis vehicula molestie felis id euismod. Nullam diam orci, mollis vitae massa eu, vestibulum vestibulum metus. Quisque bibendum, orci id vulputate mattis, tortor lectus commodo metus, ut hendrerit est lacus sit amet sapien.')
    
    g.user = u7
    Follow.create_new_follow(other_user=u1)
    Follow.create_new_follow(other_user=u2)
    Follow.create_new_follow(other_user=u4)
    Follow.create_new_follow(other_user=u5)
    
    p15 = Post.create_new_post(game_id=3070,
                         title='Curabitur arcu sapien, blandit eget malesuada at, interdum non arcu',
                         content='Donec ultrices porta purus eu venenatis. Vivamus ut ultrices odio. Praesent congue eget mi ut placerat. Praesent sit amet pulvinar elit. Aenean ex nisi, sollicitudin eu ultricies id, varius tristique turpis. Morbi mollis euismod dui. Quisque consectetur sapien metus, dignissim dictum augue vehicula in. Donec non malesuada orci, eu ornare nunc. Quisque tristique et tortor sit amet interdum. Phasellus ac metus arcu.')

    p16 = Post.create_new_post(game_id=4535,
                         title='Duis feugiat enim vel porttitor sodales',
                         content='Duis vitae vehicula tellus. Proin placerat non sapien vitae blandit. Aenean venenatis tortor id arcu mollis vestibulum. Fusce sed odio vitae leo placerat dapibus. Donec nec consectetur lacus, volutpat interdum nunc. Suspendisse lectus lectus, auctor vel leo eu, malesuada rhoncus dui. Duis felis tortor, vulputate ut porttitor id, accumsan vel justo. Mauris a tellus a erat lacinia vestibulum. Suspendisse luctus felis non nibh cursus rutrum. Sed tempus mauris ac consectetur consectetur.')

    
    g.user = u8
    Follow.create_new_follow(other_user=u1)
    Follow.create_new_follow(other_user=u4)
    Follow.create_new_follow(other_user=u6)
    Follow.create_new_follow(other_user=u9)
    Follow.create_new_follow(other_user=u10)
    
    p17 = Post.create_new_post(game_id=375231,
                         title='Fusce sed odio vitae leo placerat dapibus',
                         content='Donec nec consectetur lacus, volutpat interdum nunc. Suspendisse lectus lectus, auctor vel leo eu, malesuada rhoncus dui. Duis felis tortor, vulputate ut porttitor id, accumsan vel justo. Mauris a tellus a erat lacinia vestibulum. Suspendisse luctus felis non nibh cursus rutrum. Sed tempus mauris ac consectetur consectetur.')

    p18 = Post.create_new_post(game_id=2093,
                         title='In euismod, velit et iaculis sagittis',
                         content='Quisque condimentum tellus vitae dui finibus, vel ultrices dui scelerisque. Aliquam sed varius turpis. In pharetra pellentesque risus ac fermentum. In laoreet vitae enim ac ultrices. In id sem consectetur, elementum neque nec, aliquet ante. Donec et lobortis diam. Etiam eu est sodales, iaculis urna at, interdum odio. Aenean vitae maximus dui. Nulla facilisi. Sed sed tempor felis. Sed at suscipit elit.')


    g.user = u9
    Follow.create_new_follow(other_user=u1)
    Follow.create_new_follow(other_user=u4)
    Follow.create_new_follow(other_user=u6)
    Follow.create_new_follow(other_user=u7)
    Follow.create_new_follow(other_user=u8)
    
    p19 = Post.create_new_post(game_id=375231,
                         title='Mauris quis porta enim',
                         content='Curabitur mollis aliquam ante, vitae porta ipsum rutrum et. Vivamus rhoncus gravida turpis, non porttitor nunc porta et. Aliquam gravida iaculis turpis, eget rutrum lorem ullamcorper non. Cras arcu dolor, volutpat eu convallis ut, gravida sed ligula. Quisque tincidunt nisl ac sapien venenatis egestas. Phasellus ut sem et ante pharetra vestibulum ac quis enim. Nam porttitor vulputate mi, porttitor viverra tellus malesuada et.')

    p20 = Post.create_new_post(game_id=427930,
                         title='Fusce a lacinia augue, nec venenatis leo',
                         content='In lobortis congue justo, non malesuada diam ullamcorper sit amet. Cras libero quam, malesuada nec sem et, mattis sollicitudin augue. Nam volutpat felis vitae leo tempor, id mattis dui lobortis. Suspendisse sapien eros, feugiat vitae lacus eu, faucibus maximus urna. Nullam scelerisque convallis lorem. Maecenas volutpat iaculis felis pharetra rutrum. Cras molestie tincidunt erat sed molestie. Pellentesque vestibulum porttitor dolor, id semper est varius at.')
    
    
    g.user = u10
    Follow.create_new_follow(other_user=u1)
    Follow.create_new_follow(other_user=u2)
    Follow.create_new_follow(other_user=u3)
    Follow.create_new_follow(other_user=u4)
    Follow.create_new_follow(other_user=u7)
    Follow.create_new_follow(other_user=u8)
    Follow.create_new_follow(other_user=u9)
    
    p21 = Post.create_new_post(game_id=2093,
                         title='Fusce ullamcorper id leo et mollis',
                         content='Cras tellus erat, elementum vitae tellus ac, dapibus porta ligula. Pellentesque mollis orci id erat tristique, eget tincidunt lectus dictum. Cras hendrerit tincidunt arcu, nec eleifend urna. In arcu diam, mattis quis porta quis, placerat et odio. Ut sed urna hendrerit, lobortis lectus ut, volutpat orci.')
   
    p22 = Post.create_new_post(game_id=4535,
                         title='Mauris ac dolor lacinia ligula posuere aliquam',
                         content='Maecenas hendrerit volutpat libero. Donec condimentum sem quis lorem sodales, finibus sagittis turpis iaculis. Nulla at metus blandit, laoreet odio a, egestas leo. In lobortis congue justo, non malesuada diam ullamcorper sit amet. Cras libero quam, malesuada nec sem et, mattis sollicitudin augue.')
   
    g.user = None
   
with app.app_context():
    u1 = User.query.get_or_404(1)
    u2 = User.query.get_or_404(2)
    u3 = User.query.get_or_404(3)
    u4 = User.query.get_or_404(4)
    u5 = User.query.get_or_404(5)
    u6 = User.query.get_or_404(6)
    u7 = User.query.get_or_404(7)
    u8 = User.query.get_or_404(8)
    u9 = User.query.get_or_404(9)
    u10 = User.query.get_or_404(10)
    p1 = Post.query.get_or_404(1)
    p2 = Post.query.get_or_404(2)
    p3 = Post.query.get_or_404(3)
    p4 = Post.query.get_or_404(4)
    p5 = Post.query.get_or_404(5)
    p6 = Post.query.get_or_404(6)
    p7 = Post.query.get_or_404(7)
    p8 = Post.query.get_or_404(8)
    p9 = Post.query.get_or_404(9)
    p10 = Post.query.get_or_404(10)
    p11 = Post.query.get_or_404(11)
    p12 = Post.query.get_or_404(12)
    p13 = Post.query.get_or_404(13)
    p14 = Post.query.get_or_404(14)
    p15 = Post.query.get_or_404(15)
    p16 = Post.query.get_or_404(16)
    p17 = Post.query.get_or_404(17)
    p18 = Post.query.get_or_404(18)
    p19 = Post.query.get_or_404(19)
    p20 = Post.query.get_or_404(20)
    p21 = Post.query.get_or_404(21)
    p22 = Post.query.get_or_404(22)
    g.user = u1
    Comment.create_new_comment(post=p4, content='Nam ut nibh justo. Mauris vel magna dui.')
    Comment.create_new_comment(post=p5, content='Nam ut nibh justo. Mauris vel magna dui.')
    Comment.create_new_comment(post=p9, content='Nam ut nibh justo. Mauris vel magna dui.')
    Comment.create_new_comment(post=p10, content='Nam ut nibh justo. Mauris vel magna dui.')
    Comment.create_new_comment(post=p18, content='Nam ut nibh justo. Mauris vel magna dui.')
    
    g.user = u2
    Comment.create_new_comment(post=p1, content='Donec non cursus quam, sit amet efficitur felis. Duis efficitur enim in mi cursus auctor.')
    Comment.create_new_comment(post=p2, content='Donec non cursus quam, sit amet efficitur felis. Duis efficitur enim in mi cursus auctor.')
    Comment.create_new_comment(post=p7, content='Donec non cursus quam, sit amet efficitur felis. Duis efficitur enim in mi cursus auctor.')
    Comment.create_new_comment(post=p12, content='Donec non cursus quam, sit amet efficitur felis. Duis efficitur enim in mi cursus auctor.')
    Comment.create_new_comment(post=p16, content='Donec non cursus quam, sit amet efficitur felis. Duis efficitur enim in mi cursus auctor.')
    Comment.create_new_comment(post=p22, content='Donec non cursus quam, sit amet efficitur felis. Duis efficitur enim in mi cursus auctor.')

    g.user = u3
    Comment.create_new_comment(post=p3, content='Fusce posuere massa sapien, ac consectetur augue suscipit sed.')
    Comment.create_new_comment(post=p6, content='Fusce posuere massa sapien, ac consectetur augue suscipit sed.')
    Comment.create_new_comment(post=p9, content='Fusce posuere massa sapien, ac consectetur augue suscipit sed.')
    Comment.create_new_comment(post=p11, content='Fusce posuere massa sapien, ac consectetur augue suscipit sed.')
    Comment.create_new_comment(post=p14, content='Fusce posuere massa sapien, ac consectetur augue suscipit sed.')
    Comment.create_new_comment(post=p17, content='Fusce posuere massa sapien, ac consectetur augue suscipit sed.')
    Comment.create_new_comment(post=p21, content='Fusce posuere massa sapien, ac consectetur augue suscipit sed.')
    
    g.user = u4
    Comment.create_new_comment(post=p4, content='Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.')
    Comment.create_new_comment(post=p7, content='Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.')
    Comment.create_new_comment(post=p13, content='Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.')
    Comment.create_new_comment(post=p16, content='Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.')
    Comment.create_new_comment(post=p18, content='Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.')
    Comment.create_new_comment(post=p22, content='Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.')

    g.user = u5
    Comment.create_new_comment(post=p1, content='Phasellus hendrerit vel mauris at rutrum. Sed vestibulum tellus et nibh molestie interdum.')
    Comment.create_new_comment(post=p5, content='Phasellus hendrerit vel mauris at rutrum. Sed vestibulum tellus et nibh molestie interdum.')
    Comment.create_new_comment(post=p10, content='Phasellus hendrerit vel mauris at rutrum. Sed vestibulum tellus et nibh molestie interdum.')
    Comment.create_new_comment(post=p12, content='Phasellus hendrerit vel mauris at rutrum. Sed vestibulum tellus et nibh molestie interdum.')
    Comment.create_new_comment(post=p15, content='Phasellus hendrerit vel mauris at rutrum. Sed vestibulum tellus et nibh molestie interdum.')
    Comment.create_new_comment(post=p20, content='Phasellus hendrerit vel mauris at rutrum. Sed vestibulum tellus et nibh molestie interdum.')
    Comment.create_new_comment(post=p22, content='Phasellus hendrerit vel mauris at rutrum. Sed vestibulum tellus et nibh molestie interdum.')

    g.user = u6
    Comment.create_new_comment(post=p2, content='Cras bibendum at leo vitae cursus. Maecenas pharetra sed felis ut commodo.')
    Comment.create_new_comment(post=p4, content='Cras bibendum at leo vitae cursus. Maecenas pharetra sed felis ut commodo.')
    Comment.create_new_comment(post=p8, content='Cras bibendum at leo vitae cursus. Maecenas pharetra sed felis ut commodo.')
    Comment.create_new_comment(post=p13, content='Cras bibendum at leo vitae cursus. Maecenas pharetra sed felis ut commodo.')
    Comment.create_new_comment(post=p16, content='Cras bibendum at leo vitae cursus. Maecenas pharetra sed felis ut commodo.')
    Comment.create_new_comment(post=p19, content='Cras bibendum at leo vitae cursus. Maecenas pharetra sed felis ut commodo.')

    g.user = u7
    Comment.create_new_comment(post=p1, content='Morbi ultrices quam eu nisl efficitur, in volutpat tortor sagittis.')
    Comment.create_new_comment(post=p6, content='Morbi ultrices quam eu nisl efficitur, in volutpat tortor sagittis.')
    Comment.create_new_comment(post=p11, content='Morbi ultrices quam eu nisl efficitur, in volutpat tortor sagittis.')
    Comment.create_new_comment(post=p14, content='Morbi ultrices quam eu nisl efficitur, in volutpat tortor sagittis.')
    Comment.create_new_comment(post=p18, content='Morbi ultrices quam eu nisl efficitur, in volutpat tortor sagittis.')
    Comment.create_new_comment(post=p20, content='Morbi ultrices quam eu nisl efficitur, in volutpat tortor sagittis.')

    g.user = u8
    Comment.create_new_comment(post=p4, content='Donec urna eros, ultricies ut mauris eget, imperdiet sodales leo.')
    Comment.create_new_comment(post=p10, content='Donec urna eros, ultricies ut mauris eget, imperdiet sodales leo.')
    Comment.create_new_comment(post=p12, content='Donec urna eros, ultricies ut mauris eget, imperdiet sodales leo.')
    Comment.create_new_comment(post=p20, content='Donec urna eros, ultricies ut mauris eget, imperdiet sodales leo.')
    Comment.create_new_comment(post=p21, content='Donec urna eros, ultricies ut mauris eget, imperdiet sodales leo.')
    Comment.create_new_comment(post=p22, content='Donec urna eros, ultricies ut mauris eget, imperdiet sodales leo.')
    
    g.user = u9
    Comment.create_new_comment(post=p2, content='Class aptent taciti sociosqu ad litora torquent per conubia nostra.')
    Comment.create_new_comment(post=p7, content='Class aptent taciti sociosqu ad litora torquent per conubia nostra.')
    Comment.create_new_comment(post=p13, content='Class aptent taciti sociosqu ad litora torquent per conubia nostra.')
    Comment.create_new_comment(post=p16, content='Class aptent taciti sociosqu ad litora torquent per conubia nostra.')
    Comment.create_new_comment(post=p21, content='Class aptent taciti sociosqu ad litora torquent per conubia nostra.')

    g.user = u10
    Comment.create_new_comment(post=p1, content='Nullam congue efficitur risus. Proin sodales ligula eget vulputate placerat.')
    Comment.create_new_comment(post=p8, content='Nullam congue efficitur risus. Proin sodales ligula eget vulputate placerat.')
    Comment.create_new_comment(post=p10, content='Nullam congue efficitur risus. Proin sodales ligula eget vulputate placerat.')
    Comment.create_new_comment(post=p6, content='Nullam congue efficitur risus. Proin sodales ligula eget vulputate placerat.')
    Comment.create_new_comment(post=p9, content='Nullam congue efficitur risus. Proin sodales ligula eget vulputate placerat.')
    Comment.create_new_comment(post=p17, content='Nullam congue efficitur risus. Proin sodales ligula eget vulputate placerat.')

    g.user = None
    
with app.app_context():
    g.user = None