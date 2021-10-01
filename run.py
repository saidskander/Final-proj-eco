#!/usr/bin/python3
"""Run File"""


from pet_shop import app  # 1


if __name__ == "__main__":  # 1
    app.run(use_reloader=True, port=5000, debug=True)  # 1
