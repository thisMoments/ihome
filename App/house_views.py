
import os
from flask import Blueprint, render_template, jsonify, session, request
from sqlalchemy import or_

from App.models import User, House, Area, Facility, HouseImage, Order
from utils import status_code


from utils.settings import UPLOAD_DIRS

house_blueprint = Blueprint('house', __name__)


@house_blueprint.route('/myhouse/', methods=['GET'])
def myhouse():
    return render_template('myhouse.html')


@house_blueprint.route('/auth_myhouse/', methods=['GET'])
def auth_myhouse():
    user = User.query.get(session['user_id'])
    if user.id_card:
        houses = House.query.filter(House.user_id==user.id).order_by(House.id.desc())
        hlist_list = []
        for house in houses:
            hlist_list.append(house.to_dict())
        return jsonify(hlist_list=hlist_list, code=status_code.OK)
    else:
        return jsonify(status_code.MYHOUSE_USER_IS_NOT_AUTH)


@house_blueprint.route('/newhouse/', methods=['GET'])
def newhouse():
    return render_template('newhouse.html')


@house_blueprint.route('/area_facility/', methods=['GET'])
def area_facility():

    areas = Area.query.all()
    area_list = [area.to_dict() for area in areas]

    facilitys = Facility.query.all()
    facility_list = [facility.to_dict() for facility in facilitys]

    return jsonify(area_list=area_list, facility_list=facility_list)


@house_blueprint.route('/newhouse/', methods=['POST'])
def user_newhouse():

    house_dict = request.form.to_dict()
    facility_ids = request.form.getlist('facility')

    house = House()
    house.user_id = session['user_id']
    house.title = house_dict.get('title')
    house.price = house_dict.get('price')
    house.area_id = house_dict.get('area_id')
    house.address = house_dict.get('address')
    house.root_count = house_dict.get('root_count')
    house.acreage = house_dict.get('acreage')
    house.unit = house_dict.get('unit')
    house.capacity = house_dict.get('capacity')
    house.beds = house_dict.get('beds')
    house.deposit = house_dict.get('deposit')
    house.min_days = house_dict.get('min_days')
    house.max_days = house_dict.get('max_days')

    if facility_ids:
        facilitys = Facility.query.filter(Facility.id.in_(facility_ids)).all()
        house.facilities = facilitys
    try:
        house.add_update()
    except:
        return jsonify(status_code.DATABASE_ERROR)
    return jsonify(code=status_code.OK, house_id=house.id)


@house_blueprint.route('/images/', methods=['POST'])
def newhouse_images():

    images = request.files.get('house_image')
    house_id = request.form.get('house_id')

    # 保存成功
    url = os.path.join(UPLOAD_DIRS, images.filename)
    images.save(url)

    image_url = os.path.join(os.path.join('/static', 'upload'), images.filename)

    house_image = HouseImage()
    house_image.house_id = house_id
    house_image.url = image_url
    try:
        house_image.add_update()
    except:
        return jsonify(status_code.DATABASE_ERROR)

    house = House.query.get(house_id)

    if not house.index_image_url:
        house.index_image_url = image_url
        try:
            house.add_update()
        except:
            return jsonify(status_code.DATABASE_ERROR)

    return jsonify(code=status_code.OK, image_url=image_url)


@house_blueprint.route('/detail/', methods=['GET'])
def detail():
    return render_template('detail.html')


@house_blueprint.route('/detail/<int:id>/', methods=['GET'])
def house_detail(id):

    house = House.query.get(id)

    facility_list = house.facilities
    facility_dict_list = [facility.to_dict() for facility in facility_list]

    booking = 1
    if 'user_id' in session:
        house.user_id = session['user_id']
        booking = 0

    return jsonify(house=house.to_full_dict(),
                   facility_list=facility_dict_list,
                   booking=booking,
                   code=status_code.OK)


@house_blueprint.route('/booking/', methods=['GET'])
def booking():
    return render_template('booking.html')


@house_blueprint.route('/index/', methods=['GET'])
def index():
    return render_template('index.html')


@house_blueprint.route('/hindex/', methods=['GET'])
def house_index():

    user_name = ''
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        user_name = user.name

    houses = House.query.order_by(House.id.desc()).all()[:5]
    hlist = [house.to_dict() for house in houses]

    areas = Area.query.all()
    alist = [area.to_dict() for area in areas]

    return jsonify(code=status_code.OK,
                   user_name=user_name,
                   hlist=hlist,
                   alist=alist)


@house_blueprint.route('/search/', methods=['GET'])
def search():
    return render_template('search.html')


@house_blueprint.route('/allsearch/', methods=['GET'])
def house_search():

    search_dict = request.args

    area_id = search_dict.get('aid')
    start_data = search_dict.get('sd')
    end_date = search_dict.get('ed')
    sort_key = search_dict.get('sk')

    houses = House.query.filter(House.area_id==area_id)

    # 对房屋houses进行处理
    orders1 = Order.query.filter(Order.begin_date>=start_data,
                                 Order.end_date<=end_date)

    orders2 = Order.query.filter(Order.begin_date<=end_date,
                                 Order.end_date>=end_date)

    orders3 = Order.query.filter(Order.begin_date<=start_data,
                                 Order.end_date>=start_data)

    orders4 = Order.query.filter(Order.begin_date<=start_data,
                                 Order.end_date>=end_date)

    orders_list1 = [o1.house_id for o1 in orders1]
    orders_list2 = [o2.house_id for o2 in orders2]
    orders_list3 = [o3.house_id for o3 in orders3]
    orders_list4 = [o4.house_id for o4 in orders4]

    orders_list = orders_list1 + orders_list2 + orders_list3 + orders_list4
    orders_list = list(set(orders_list))
    # orders = Order.query.filter(or_(Order.begin_date<=end_date,
    #                                 Order.end_date>=start_data))

    # order_list = [order.house_id for order in orders]

    houses = houses.filter(House.id.notin_(orders_list))

    if sort_key:
        if sort_key == 'booking':
            sort_key = House.room_count.desc()
        if sort_key == 'price-inc':
            sort_key = House.price.asc()
        if sort_key == 'price-des':
            sort_key = House.price.desc()
    else:
        sort_key = House.house_id.desc()

    houses = houses.order_by(sort_key)

    hlist = [house.to_dict() for house in houses]

    areas = Area.query.all()
    alist = [area.to_dict() for area in areas]

    return jsonify(code=status_code.OK,
                   hlist=hlist,
                   alist=alist)


