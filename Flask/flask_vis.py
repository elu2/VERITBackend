from flask import Flask, render_template, url_for, request, redirect
from Query import llNetxQuery, SingleQuery, DictChecker, NetxSingleQuery
from Visualization import to_json, to_json_netx


app = Flask(__name__)

@app.route('/', methods=["POST","GET"])
def home():
    if request.method=="POST":
        query_type=request.form["query_type"]
        if query_type=="Dijkstra's algorithm":
            return redirect(url_for("make_bfs_query"))
        else:
            return redirect(url_for("make_single_query"))
    else:
        return render_template("home.html")

@app.route('/bfs', methods=["POST","GET"])                              
def make_bfs_query():
    if request.method=="POST":
        query_string=request.form["query_string"]
        max_linkers=int(request.form["max_linkers"])
                 
        return redirect(url_for("bfs_query_result",query_string=query_string, max_linkers=max_linkers))
    else:
        return render_template("bfs_search.html")
    
@app.route('/single_query', methods=["POST","GET"])                              
def make_single_query():
    if request.method=="POST":
        query=request.form["query"]
        depth=request.form["depth"]
        thickness_bound=request.form["thickness_bound"]
        return redirect(url_for("single_query_result",query=query, depth=depth, thickness_bound=thickness_bound))
    else:
        return render_template("single_search.html")
    

@app.route('/<query_string>/<max_linkers>')
def bfs_query_result(query_string, max_linkers):
    queries_id=query_string.split(",")
    not_in=DictChecker.check(queries_id)
    
    #Add try-except/other verification in the future to make sure it's an int
    max_linkers=int(max_linkers)
    
    llNetxQuery.query(queries_id, max_linkers)
    no_path_file=open("no_path.txt","r")
    no_path=[line.rstrip("\n") for line in no_path_file]
    
    elements=to_json_netx.clean()
    return render_template("bfs_result.html", elements=elements, no_path=no_path, not_in=not_in)



@app.route('/<query>/<depth>/<thickness_bound>')
def single_query_result(query, depth, thickness_bound):
    #Add a redirect for if you can't find the id
    #Add try-except/other verification in the future to make sure it's an int
    depth=int(depth)
    thickness_bound=int(thickness_bound)
    
   
    SingleQuery.query(query, depth, thickness_bound)
    elements=to_json.clean()
    return render_template("single_query_result.html", elements=elements)


if __name__=="__main__":
    app.run(debug=True)
    
    
    
