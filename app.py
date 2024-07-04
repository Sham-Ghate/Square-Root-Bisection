from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"

def square_root_bisection(square_target, tolerance=1e-7, max_iterations=100):
    if square_target < 0:
        raise ValueError('Square root of negative number is not defined in real numbers')
    
    if square_target in [0, 1]:
        return square_target
    
    low, high = 0, max(1, square_target)
    root = None
    
    for iteration in range(max_iterations):
        mid = (low + high) / 2
        square_mid = mid**2

        if abs(square_mid - square_target) < tolerance:
            root = mid
            break
        elif square_mid < square_target:
            low = mid
        else:
            high = mid
    
    if root is None:
        return f"Failed to converge within {max_iterations} iterations."
    else:
        return f'The square root of {square_target} is approximately {root}'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            square_target = float(request.form['square_target'])
            tolerance = float(request.form['tolerance']) if request.form['tolerance'] else 1e-7
            max_iterations = int(request.form['max_iterations']) if request.form['max_iterations'] else 100
            
            result = square_root_bisection(square_target, tolerance, max_iterations)
            flash(result)
        except ValueError as e:
            flash(f"Error: {e}")
        
        return redirect(url_for('index'))
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
