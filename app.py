from flask import Flask, render_template, request
import os
import chardet

app = Flask(__name__)

@app.route('/files/<filename>', methods=['GET'])
def read_file(filename):
    start_line = request.args.get('start_line', type=int)
    end_line = request.args.get('end_line', type=int)

    try:
        # Read the encoding of the file
        with open(os.path.join('files', filename), 'rb') as f:
            raw_data = f.read()
            encoding = chardet.detect(raw_data)['encoding']

        # Open the file with detected encoding
        with open(os.path.join('files', filename), 'r', encoding=encoding) as file:
            lines = file.readlines()
            if start_line is not None and end_line is not None:
                lines = lines[start_line-1:end_line]
            elif start_line is not None:
                lines = lines[start_line-1:]
            elif end_line is not None:
                lines = lines[:end_line]

            return render_template('index.html', content=lines)
    except FileNotFoundError:
        return render_template('error.html', error='File not found')
    except Exception as e:
        return render_template('error.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
