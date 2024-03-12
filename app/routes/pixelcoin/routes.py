# -*- coding: utf-8 -*-
from flask import redirect, url_for, render_template, abort, current_app
from flask import request as flask_request
from app import db, models, w3
import app.routes.funcs as funcs
import json
import re
import math
from datetime import date
from requests import HTTPError
from app.routes.pixelcoin import bp
import app.models as models
from eth_abi import abi

global pixelcoin

@ bp.route("/pixelcoin/<address>/", methods=["GET", "POST"])
@ bp.route("/€<address>/", methods=["GET", "POST"])
def pixelcoin(address):
    pixelcoin = models.PixelCoin.query.filter_by(address=address).first_or_404()
    return render_template("pixelcoin/profile.html", pixelcoin=pixelcoin, navbar=True, background=True, size="medium", models=models)

@ bp.route("/pixelcoin/<address>/timeline/", methods=["GET"])
@ bp.route("/€<address>/timeline/", methods=["GET"])
def timeline(address):
    return pixelcoin(address)

@ bp.route("/pixelcoin/<address>/structure/", methods=["GET"])
@ bp.route("/€<address>/structure/", methods=["GET"])
def structure(address):
    return pixelcoin(address)

@ bp.route("/pixelcoin/<address>/deposit/", methods=["GET"])
@ bp.route("/€<address>/deposit/", methods=["GET"])
def deposit(address):
    return pixelcoin(address)

@ bp.route("/pixelcoin/<address>/transfer/", methods=["GET"])
@ bp.route("/€<address>/transfer/", methods=["GET"])
def transfer(address):
    return pixelcoin(address)

@ bp.route("/pixelcoin/<address>/assign/", methods=["GET"])
@ bp.route("/€<address>/assign/", methods=["GET"])
def assign(address):
    return pixelcoin(address)

@ bp.route("/pixelcoin/<address>/revoke/", methods=["GET"])
@ bp.route("/€<address>/revoke/", methods=["GET"])
def revoke(address):
    return pixelcoin(address)

@ bp.route("/pixelcoin/<address>/claim/", methods=["GET"])
@ bp.route("/€<address>/claim/", methods=["GET"])
def claim(address):
    return pixelcoin(address)

@ bp.route("/pixelcoin/<address>/distribute/", methods=["GET"])
@ bp.route("/€<address>/distribute/", methods=["GET"])
def distribute(address):
    return pixelcoin(address)

@ bp.route("/pixelcoin/<address>/vote/", methods=["GET"])
@ bp.route("/€<address>/vote/", methods=["GET"])
def vote(address):
    return pixelcoin(address)

@ bp.route("/pixelcoin/<address>/propose/", methods=["GET"])
@ bp.route("/€<address>/propose/", methods=["GET"])
def propose(address):
    return pixelcoin(address)

@ bp.route("/pixelcoin/<address>/structure/banks/", methods=["GET"])
@ bp.route("/€<address>/structure/banks/", methods=["GET"])
def banks(address):
    return pixelcoin(address)

@ bp.route("/pixelcoin/<address>/structure/permits/", methods=["GET"])
@ bp.route("/€<address>/structure/permits/", methods=["GET"])
def permits(address):
    return pixelcoin(address)

@ bp.route("/pixelcoin/<address>/structure/dividends/", methods=["GET"])
@ bp.route("/€<address>/structure/dividends/", methods=["GET"])
def dividends(address):
    return pixelcoin(address)

@ bp.route("/pixelcoin/<address>/structure/referendums/", methods=["GET"])
@ bp.route("/€<address>/structure/referendums/", methods=["GET"])
def referendums(address):
    return pixelcoin(address)

@ bp.route("/pixelcoin/<address>/ownership/", methods=["GET"])
@ bp.route("/€<address>/ownership/", methods=["GET"])
def ownership(address):
    return pixelcoin(address)

@bp.route("/pixelcoin/<address>/mint/", methods=["GET","POST"])
@bp.route("/€<address>/mint/", methods=["GET","POST"])
def mint(address):
    if flask_request.method == 'POST':
        tx = flask_request.form.get("tx")
        receipt = w3.eth.waitForTransactionReceipt(tx)
        log = receipt.logs[0]
        print(f"Receipt: {receipt.contractAddress} != Address: {address}")
        print(f"Log: {log}")
        assert(log["address"] == address)
        account, amount = abi.decode_abi(["address","uint256"],bytes.fromhex(log["data"][2:]))
        print(account,amount)
        pixelcoin = models.PixelCoin.query.filter_by(address=address).first()
        pixelcoin.update_ownership()
        return json.dumps({'status': 'success'})

    return pixelcoin(address)

@ bp.route("/pixelcoin/<address>/photo/", methods=["GET"])
@ bp.route("/€<address>/photo/", methods=["GET"])
def photo(address):
    return pixelcoin(address)

@ bp.route("/pixelcoin/<address>/update/timeline/", methods=["POST"])
@ bp.route("/€<address>/update/timeline/", methods=["POST"])
def update_timeline(address):
    pixelcoin = models.PixelCoin.query.filter_by(address=address).first()
    if not pixelcoin:
        abort(404)
    pixelcoin.update_timeline()
    db.session.commit()
    return json.dumps({'status': 'success'})


@bp.route("/pixelcoin/<address>/get/timeline/", methods=["GET"])
@bp.route("/€<address>/get/timeline/", methods=["GET"])
def get_timeline(address):
    pixelcoin = models.PixelCoin.query.filter_by(address=address).first_or_404()
    return render_template("pixelcoin/timeline.html", pixelcoin=pixelcoin, models=models)


@ bp.route("/pixelcoin/<address>/update/ownership/", methods=["POST"])
@ bp.route("/€<address>/update/ownership/", methods=["POST"])
def update_ownership(address):
    pixelcoin = models.PixelCoin.query.filter_by(address=address).first()
    if not pixelcoin:
        abort(404)
    pixelcoin.update_ownership()
    db.session.commit()
    return json.dumps({'status': 'success'})

@bp.route("/pixelcoin/<address>/get/ownership/", methods=["GET"])
@bp.route("/€<address>/get/ownership/", methods=["GET"])
def get_ownership(address):
    pixelcoin = models.PixelCoin.query.filter_by(address=address).first_or_404()
    return render_template("pixelcoin/ownership/load-ownership-chart.html", pixelcoin=pixelcoin)

@ bp.route("/pixelcoin/<address>/update/structure/", methods=["POST"])
@ bp.route("/€<address>/update/structure/", methods=["POST"])
def update_structure(address):
    pixelcoin = models.PixelCoin.query.filter_by(address=address).first()
    if not pixelcoin:
        abort(404)
    pixelcoin.update_structure()
    db.session.commit()
    return json.dumps({'status': 'success'})

@bp.route("/pixelcoin/<address>/get/structure/", methods=["GET"])
@bp.route("/€<address>/get/structure/", methods=["GET"])
def get_structure(address):
    pixelcoin = models.PixelCoin.query.filter_by(address=address).first_or_404()
    return render_template("pixelcoin/structure.html", pixelcoin=pixelcoin,models=models)

@bp.route("/pixelcoin/<address>/get/structure/bank/transfer/", methods=["GET"])
@bp.route("/€<address>/get/structure/bank/transfer/", methods=["GET"])
def get_transfer(address):
    pixelcoin = models.PixelCoin.query.filter_by(address=address).first_or_404()
    return render_template("pixelcoin/structure/transfer.html", pixelcoin=pixelcoin,models=models)

@bp.route("/pixelcoin/<address>/get/edit/", methods=["GET"])
@bp.route("/€<address>/get/edit/", methods=["GET"])
def get_edit(address):
    pixelcoin = models.PixelCoin.query.filter_by(address=address).first_or_404()
    return render_template("pixelcoin/edit.html", pixelcoin=pixelcoin,models=models)