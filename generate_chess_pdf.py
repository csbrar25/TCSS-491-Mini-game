CHESS_PDF_TEMPLATE = r"""
%PDF-1.6

% Root
1 0 obj
<<
  /AcroForm <<
    /DA (/ArialUnicodeMS 14 Tf 0 0 0 rg)  % Ensures correct Unicode rendering
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
    /Font << /F1 5 0 R >>  
  >>
  /Rotate 0
  /Type /Page
>>
endobj

3 0 obj
<< >>
stream
endstream
endobj

21 0 obj
[
  ###FIELD_LIST###
]
endobj

42 0 obj
<< >>
stream
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

function select_piece(x, y) {
    var piece = board[y][x];
    if (piece !== '' && (
         (current_turn === 'white' && piece.charCodeAt(0) < 9818) ||
         (current_turn === 'black' && piece.charCodeAt(0) >= 9818)
       )) {
        selected_piece = piece;
        selected_x = x;
        selected_y = y;
    }
}

function move_piece(x, y) {
    if (selected_piece !== null) {
        board[y][x] = selected_piece;
        board[selected_y][selected_x] = '';
        selected_piece = null;
        selected_x = -1;
        selected_y = -1;
        current_turn = (current_turn === 'white') ? 'black' : 'white';
        draw_board();
    }
}

function squareClicked(x, y) {
    if (selected_piece === null && board[y][x] !== '') {
        select_piece(x, y);
    } else if (selected_piece !== null) {
        move_piece(x, y);
    }
}

function draw_board() {
    for (var y = 0; y < 8; y++) {
        for (var x = 0; x < 8; x++) {
            var fld = this.getField('B_' + x + '_' + y);
            if (fld) {
                fld.value = String.fromCharCode(board[y][x].charCodeAt(0));
            }
        }
    }
}

draw_board();
endstream
endobj

trailer
<<
  /Root 1 0 R
>>
%%EOF
"""

CHESS_BUTTON_TEMPLATE = r"""
###IDX### obj
<<
  /FT /Btn
  /Ff 65536
  /MK << /CA (###LABEL###) /BG [###BG_COLOR###] /BC [0 0 0] >>
  /DA (/ArialUnicodeMS 14 Tf 0 0 0 rg)
  /A << /JS (squareClicked(###X###, ###Y###);) /S /JavaScript >>
  /P 16 0 R
  /Rect [###RECT###]
  /Subtype /Widget
  /T (B_###X###_###Y###)
  /Type /Annot
  /Border [1 1 1]
>>
endobj
"""

GRID_SIZE = 60
BOARD_OFFSET_X = 50
BOARD_OFFSET_Y = 700

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
    obj_idx_ctr = 50  

    for y in range(8):
        for x in range(8):
            button = CHESS_BUTTON_TEMPLATE
            button = button.replace("###IDX###", f"{obj_idx_ctr} 0")
            label = initial_board[y][x] if initial_board[y][x] else " "
            button = button.replace("###LABEL###", label)
            bg_color = "1 1 1" if (x + y) % 2 == 0 else "0.5 0.5 0.5"
            button = button.replace("###BG_COLOR###", bg_color)
            llx = BOARD_OFFSET_X + x * GRID_SIZE
            lly = BOARD_OFFSET_Y - (8 - y) * GRID_SIZE
            urx = BOARD_OFFSET_X + (x + 1) * GRID_SIZE
            ury = BOARD_OFFSET_Y - (7 - y) * GRID_SIZE
            button = button.replace("###RECT###", f"{llx} {lly} {urx} {ury}")
            
            fields_text += button + "\n"
            field_indexes.append(f"{obj_idx_ctr} 0 R")
            obj_idx_ctr += 1

    filled_pdf = CHESS_PDF_TEMPLATE.replace("###FIELDS###", fields_text)
    filled_pdf = filled_pdf.replace("###FIELD_LIST###", " ".join(field_indexes))
    
    with open("chess_game.pdf", "w", encoding="utf-8") as pdf_file:
        pdf_file.write(filled_pdf)

if __name__ == '__main__':
    generate_chess_pdf()