import difflib
import logging
import os
import socket

import dns.name
import dns.resolver
from flask import Blueprint, jsonify, request, url_for

import communication_service as network
import convert as cv

logger = logging.getLogger(__name__)

api = Blueprint("api", __name__, url_prefix="/api")

_CONTENT_TYPE_MAP = {
    "text/csv": cv.csv_para_pdf,
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": cv.excel_para_pdf,
    "application/vnd.ms-excel": cv.excel_para_pdf,
    "image/png": cv.imagem_para_pdf,
    "image/jpeg": cv.imagem_para_pdf,
    "image/jpg": cv.imagem_para_pdf,
    "text/plain": cv.texto_para_pdf,
}


@api.route("/dns", methods=["POST"])
def dns_api():
    hostname = request.form.get("dns", "").strip()
    try:
        status = network.resolve_dns(hostname)
        return jsonify({"dns": hostname, "status": status})
    except dns.resolver.NoAnswer:
        return jsonify({"dns": hostname, "status": ["Sem resposta"]})
    except dns.resolver.NXDOMAIN:
        return jsonify({"dns": hostname, "status": ["DNS inválido"]})
    except dns.name.EmptyLabel:
        return jsonify({"dns": hostname, "status": ["DNS inválido"]})
    except Exception as e:
        logger.exception("API DNS error: %s", hostname)
        return jsonify({"error": str(e)}), 500


@api.route("/combo", methods=["POST"])
def combo_api():
    ip = request.form.get("ip", "").strip()
    ports_str = request.form.get("portas", "").strip()

    if not ip:
        return jsonify({"error": "Informe um servidor ou IP"}), 400
    if not ports_str:
        return jsonify({"error": "Informe ao menos uma porta"}), 400

    try:
        port_list, status_list, color_list = network.check_ports(ip, ports_str)

        if not port_list:
            return jsonify({"error": "Nenhuma porta válida informada"}), 400

        addr_info = socket.getaddrinfo(ip, None)
        resolved_ip = addr_info[0][4][0] if addr_info else ip

        try:
            dns_routes = network.resolve_dns(ip)
        except Exception:
            dns_routes = []

        return jsonify(
            {
                "ip": ip,
                "port_list": port_list,
                "status_list": status_list,
                "color_list": color_list,
                "resolved_ip": resolved_ip,
                "dns_routes": dns_routes,
            }
        )
    except socket.gaierror:
        return jsonify({"error": f"Servidor '{ip}' inválido ou não encontrado"}), 400
    except UnicodeError:
        return jsonify({"error": f"Servidor '{ip}' inválido"}), 400
    except Exception as e:
        logger.exception("API Combo error: %s", ip)
        return jsonify({"error": str(e)}), 500


@api.route("/diff", methods=["POST"])
def diff_api():
    input1 = request.form.get("input1", "")
    input2 = request.form.get("input2", "")
    diffs = list(difflib.ndiff(input1.splitlines(), input2.splitlines()))

    left: list[dict] = []
    right: list[dict] = []
    left_num = 0
    right_num = 0
    removed_buf: list[str] = []
    added_buf: list[str] = []

    def flush_buffers() -> None:
        nonlocal left_num, right_num
        for i in range(max(len(removed_buf), len(added_buf))):
            if i < len(removed_buf):
                left_num += 1
                left.append(
                    {"num": left_num, "text": removed_buf[i], "kind": "removed"}
                )
            else:
                left.append({"num": "", "text": "", "kind": "empty"})

            if i < len(added_buf):
                right_num += 1
                right.append({"num": right_num, "text": added_buf[i], "kind": "added"})
            else:
                right.append({"num": "", "text": "", "kind": "empty"})

        removed_buf.clear()
        added_buf.clear()

    for line in diffs:
        if line.startswith("? "):
            continue
        tag = line[:2]
        text = line[2:]

        if tag == "- ":
            removed_buf.append(text)
        elif tag == "+ ":
            added_buf.append(text)
        else:
            flush_buffers()
            left_num += 1
            right_num += 1
            left.append({"num": left_num, "text": text, "kind": "unchanged"})
            right.append({"num": right_num, "text": text, "kind": "unchanged"})

    flush_buffers()

    return jsonify({"left": left, "right": right})


@api.route("/convert", methods=["POST"])
def convert_api():
    file = request.files.get("file")
    if not file or not file.filename:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    converter = _CONTENT_TYPE_MAP.get(file.content_type)
    if not converter:
        return jsonify({"error": "Formato de arquivo não suportado"}), 400

    pdf_name = os.path.splitext(file.filename)[0].lower() + ".pdf"

    try:
        pdf_buffer = converter(file, titulo_pdf=pdf_name)
    except Exception as e:
        logger.exception("API Convert error: %s", file.filename)
        return jsonify({"error": f"Erro ao converter: {e}"}), 500

    output_dir = os.path.join("static", "convertidos")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, pdf_name)

    with open(output_path, "wb") as f:
        f.write(pdf_buffer.read())

    download_url = url_for("static", filename=f"convertidos/{pdf_name}", _external=True)
    return jsonify({"download_url": download_url, "filename": pdf_name})
