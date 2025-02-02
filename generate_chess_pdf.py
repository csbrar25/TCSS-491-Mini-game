#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Revised Chess PDF generator – inspired by the provided Tetris PDF code structure

CHESS_PDF_TEMPLATE = r"""
%PDF-1.6

% Root
1 0 obj
<<
  /AcroForm <<
    /DA (/Helv 14 Tf 0 0 0 rg)
    /Fields [ ###FIELD_LIST### ]
  >>
  /Pages 2 0 R
  /OpenAction 42 0 R
  /Type /Catalog
>>
endobj

2 0 obj
<<
  /Count 1
  /Kids [ 16 0 R ]
  /Type /Pages
>>
endobj

###FIELDS###

%% Chessboard Page
16 0 obj
<<
  /Annots 21 0 R
  /Contents 3 0 R
  /CropBox [0 0 612 792]
  /MediaBox [0 0 612 792]
  /Parent 2 0 R
  /Resources <<
    /Font << /F1 5 0 R >>  % (Optional: You can define or embed a font here)
  >>
  /Rotate 0
  /Type /Page
>>
endobj

3 0 obj
<< >>
stream
% (Empty content stream – board is drawn using form fields.)
endstream
endobj

21 0 obj
[
  ###FIELD_LIST###
]
endobj

%% Document–level JavaScript for Chess Logic
42 0 obj
<< >>
stream
// Chessboard state and logic

// 8x8 board: row 0 = top row
var board = [
  ['♜','♞','♝','♛','♚','♝','♞','♜'],
  ['♟','♟','♟','♟','♟','♟','♟','♟'],
  ['','','','','','','',''],
  ['','','','','','','',''],
  ['','','','','','','',''],
  ['','','','','','','',''],
  ['♙','♙','♙','♙','♙','♙','♙','♙'],
  ['♖','♘','♗','♕','♔','♗','♘','♖']
];

var selected_piece = null;
var selected_x = -1;
var selected_y = -1;
var current_turn = 'white';

// Given a square (x,y), select its piece if it belongs to the player whose turn it is.
function select_piece(x, y) {
    var piece = board[y][x];
    // Unicode for white pieces: U+2654 to U+2659 (decimal 9812-9817)
    // Unicode for black pieces: U+265A to U+265F (decimal 9818-9823)
    if (piece !== '' && (
         (current_turn === 'white' && piece.charCodeAt(0) < 9818) ||
         (current_turn === 'black' && piece.charCodeAt(0) >= 9818)
       )) {
        selected_piece = piece;
        selected_x = x;
        selected_y = y;
    }
}

// Move a selected piece to (x,y) and switch turns.
function move_piece(x, y) {
    if (selected_piece !== null) {
        // (Additional move validations can be added here.)
        board[y][x] = selected_piece;
        board[selected_y][selected_x] = '';
        selected_piece = null;
        selected_x = -1;
        selected_y = -1;
        current_turn = (current_turn === 'white') ? 'black' : 'white';
        draw_board();
    }
}

// This function is invoked when any square is clicked.
function squareClicked(x, y) {
    if (selected_piece === null && board[y][x] !== '') {
        select_piece(x, y);
    } else if (selected_piece !== null) {
        move_piece(x, y);
    }
}

// Update all the button fields to display the current board state.
function draw_board() {
    for (var y = 0; y < 8; y++) {
        for (var x = 0; x < 8; x++) {
            var fld = this.getField('B_' + x + '_' + y);
            if (fld) {
                fld.value = board[y][x];
            }
        }
    }
}

// Initialize board when the PDF opens.
draw_board();
endstream
endobj

trailer
<<
  /Root 1 0 R
>>
%%EOF
"""

# Template for each chess square button.
# Note the added /DA entry for default appearance.
CHESS_BUTTON_TEMPLATE = r"""
###IDX### obj
<<
  /FT /Btn
  /Ff 65536
  /MK << /CA (###LABEL###) >>
  /DA (/Helv 14 Tf 0 0 0 rg)
  /A << /JS (squareClicked(###X###, ###Y###);) /S /JavaScript >>
  /P 16 0 R
  /Rect [###RECT###]
  /Subtype /Widget
  /T (B_###X###_###Y###)
  /Type /Annot
>>
endobj
"""

# Board layout constants (adjust these as needed).
GRID_SIZE = 60
BOARD_OFFSET_X = 50
BOARD_OFFSET_Y = 600

# Initial board state for setting up labels in the PDF.
initial_board = [
    ['♜','♞','♝','♛','♚','♝','♞','♜'],
    ['♟','♟','♟','♟','♟','♟','♟','♟'],
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['♙','♙','♙','♙','♙','♙','♙','♙'],
    ['♖','♘','♗','♕','♔','♗','♘','♖']
]

def generate_chess_pdf():
    fields_text = ""
    field_indexes = []
    obj_idx_ctr = 50  # Starting object number for square fields.

    # Create a button (form field) for every square on the chess board.
    for y in range(8):
        for x in range(8):
            button = CHESS_BUTTON_TEMPLATE
            button = button.replace("###IDX###", f"{obj_idx_ctr} 0")
            # If the square is empty, use a space so that Acrobat renders it.
            label = initial_board[y][x] if initial_board[y][x] else " "
            button = button.replace("###LABEL###", label)
            button = button.replace("###X###", str(x))
            button = button.replace("###Y###", str(y))
            # Calculate the rectangle for the square.
            # (PDF coordinate origin is the bottom–left corner.)
            llx = BOARD_OFFSET_X + x * GRID_SIZE
            lly = BOARD_OFFSET_Y - (y + 1) * GRID_SIZE
            urx = BOARD_OFFSET_X + (x + 1) * GRID_SIZE
            ury = BOARD_OFFSET_Y - y * GRID_SIZE
            button = button.replace("###RECT###", f"{llx} {lly} {urx} {ury}")
            
            fields_text += button + "\n"
            field_indexes.append(f"{obj_idx_ctr} 0 R")
            obj_idx_ctr += 1

    # Insert the fields and list of field references into the PDF template.
    filled_pdf = CHESS_PDF_TEMPLATE.replace("###FIELDS###", fields_text)
    filled_pdf = filled_pdf.replace("###FIELD_LIST###", " ".join(field_indexes))
    
    # Write out the PDF file.
    with open("chess_game.pdf", "w", encoding="utf-8") as pdf_file:
        pdf_file.write(filled_pdf)

if __name__ == '__main__':
    generate_chess_pdf()
