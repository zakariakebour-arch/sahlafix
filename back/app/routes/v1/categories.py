from flask import Blueprint,request,jsonify

category_bp = Blueprint("categories_v1",__name__,url_prefix="/api/v1/categories")

#Creamos la primera funcion que devuelve categorias
@category_bp.route("/",methods=["GET"])
def get_categories():
    
    return jsonify({"data":[]}),200