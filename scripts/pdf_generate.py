from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def create_pdf(words_list, size, puzzles_per_page, solutions_location, solutions_per_page, font_size, include_logo):
    buffer = BytesIO()
    pagesize = A4 if size == 'A4' else letter
    p = canvas.Canvas(buffer, pagesize=pagesize)
    
    # Añadir página de título para las sopas de letras
    add_title_page(p, "SOPAS DE LETRAS", pagesize)
    
    p.setFont("Helvetica", font_size)
    
    puzzles_drawn = 0
    for i, words in enumerate(words_list):
        cat = words.pop(0)
        if puzzles_drawn % puzzles_per_page == 0 and puzzles_drawn != 0:
            p.showPage()
        position = puzzles_drawn % puzzles_per_page
        draw_decorations(p, pagesize)
        draw_puzzle(p, words, title=f"{cat}", font_size=font_size, position=position, puzzles_per_page=puzzles_per_page)
        words.insert(0, cat)
        puzzles_drawn += 1
    
    if solutions_location == 'end':
        p.showPage()
        
        # Añadir página de título para las respuestas
        add_title_page(p, "RESPUESTAS DE LAS SOPAS DE LETRAS", pagesize)
        
        solutions_drawn = 0
        for i, words in enumerate(words_list):
            cat = words.pop(0)
            if solutions_drawn % solutions_per_page == 0 and solutions_drawn != 0:
                p.showPage()
            position = solutions_drawn % solutions_per_page
            draw_decorations(p, pagesize)
            draw_solution_page(p, words, title=f"{cat}", font_size=font_size, position=position)
            solutions_drawn += 1
    
    p.save()
    buffer.seek(0)
    return buffer

def add_title_page(canvas, title, pagesize):
    width, height = pagesize
    title_font_size = 36
    canvas.setFont("Helvetica-Bold", title_font_size)
    canvas.setFillColorRGB(0, 0, 0)  # Color negro para el título
    draw_decorations(canvas, pagesize)
    canvas.drawCentredString(width / 2, height / 2, title)
    canvas.showPage()

def draw_puzzle(canvas, words, title="", font_size=14, position=0, puzzles_per_page=1):
    puzzle, solution = generate_word_search(words)
    pagesize = canvas._pagesize
    width, height = pagesize
    
    title_font_size = font_size + 4
    canvas.setFont("Helvetica-Bold", title_font_size)
    canvas.setFillColorRGB(0, 0, 0)  # Color negro para el título
    
    if puzzles_per_page == 1:
        start_x = width * 0.1
        start_y = height * 0.85
        words_x = width * 0.8
    else:
        start_x = width * 0.1
        start_y = height * (0.85 - 0.4 * position)
        words_x = width * 0.1 if position == 1 else width * 0.8
    
    canvas.drawCentredString(width / 2, start_y + 40, title)
    draw_grid(canvas, puzzle, font_size, start_x, start_y)
    draw_words_list(canvas, words, font_size - 2, words_x, start_y)

def draw_solution_page(canvas, solution, title="", font_size=14, position=0):
    pagesize = canvas._pagesize
    width, height = pagesize

    title_font_size = font_size + 4
    canvas.setFont("Helvetica-Bold", title_font_size)
    canvas.setFillColorRGB(0, 0, 0)  # Color negro para el título
    
    col = position % 2
    row = position // 2
    start_x = width * (0.1 + 0.45 * col)
    start_y = height * (0.85 - 0.4 * row)

    canvas.drawCentredString(start_x + width * 0.225, start_y + 40, title)
    draw_grid(canvas, solution, font_size, start_x, start_y, color=(0, 0, 0))  # Color negro para la solución

def draw_grid(canvas, grid, font_size=14, start_x=100, start_y=700, color=(0, 0, 0)):
    size = len(grid)
    cell_size = 20

    canvas.setFont("Helvetica", font_size)
    canvas.setFillColorRGB(*color)

    for i in range(size):
        for j in range(len(grid[i])):
            x = start_x + j * cell_size
            y = start_y - i * cell_size
            if j < len(grid[i]):
                canvas.drawString(x, y, grid[i][j])
            canvas.rect(x - 2, y - 15, cell_size, cell_size)

def draw_words_list(canvas, words, font_size, start_x, start_y):
    canvas.setFont("Helvetica", font_size)  # Fuente normal para las palabras
    canvas.setFillColorRGB(0, 0, 0)  # Color negro para las palabras
    y_offset = 0

    for word in words:
        canvas.drawString(start_x, start_y - y_offset, word)
        y_offset += font_size + 2  # Espacio entre las palabras

def draw_decorations(canvas, pagesize):
    width, height = pagesize
    canvas.setLineWidth(1)
    
    # Bordes decorativos
    canvas.setStrokeColorRGB(0, 0, 0)
    canvas.rect(20, 20, width - 40, height - 40)
    
    # Encabezado y pie de página
    canvas.setFont("Helvetica", 10)
    #canvas.drawString(30, height - 30, "Sopas de Letras")
    canvas.drawRightString(width - 30, height - 30, "Página %d" % canvas.getPageNumber())
    #canvas.drawString(30, 20, "Generated with ReportLab")

