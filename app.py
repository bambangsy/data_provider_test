from data_processing import cluster_group_1
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/cluster1')
def get_cluster_1():
    return jsonify(cluster_group_1[0])

@app.route('/cluster2')
def get_cluster_2():
    return jsonify(cluster_group_1[1])

@app.route('/cluster3')
def get_cluster_3():
    return jsonify(cluster_group_1[2])


if __name__ == '__main__':
    app.run(debug=True)




