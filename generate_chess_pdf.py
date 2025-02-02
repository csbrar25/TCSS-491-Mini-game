import re

CHESS_PDF_TEMPLATE = r"""
%PDF-1.6

1 0 obj
<<
  /Type /Catalog
  /Pages 2 0 R
  /AcroForm <<
    /Fields [ ###FIELD_LIST### ]
    /DA (/F1 14 Tf 0 0 0 rg)
    /DR <<
      /Font <<
        /F1 5 0 R
      >>
    >>
  >>
  /OpenAction <<
    /S /JavaScript
    /JS (
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
      
      function draw_board() {
        for (var y = 0; y < 8; y++) {
          for (var x = 0; x < 8; x++) {
            var fld = this.getField('B_' + x + '_' + y);
            if (fld) fld.value = board[y][x];
          }
        }
      }
      
      function select_piece(x, y) {
        var piece = board[y][x];
        if (piece !== '' && (
          (current_turn === 'white' && piece.charCodeAt(0) < 9818) ||
          (current_turn === 'black' && piece.charCodeAt(0) >= 9818)
        )) {
          selected_piece = piece;
          selected_x = x;
          selected_y = y;
          return true;
        }
        return false;
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
        if (selected_piece === null) {
          select_piece(x, y);
        } else {
          move_piece(x, y);
        }
      }
      
      draw_board();
    )
  >>
>>
endobj

2 0 obj
<<
  /Type /Pages
  /Kids [ 3 0 R ]
  /Count 1
>>
endobj

3 0 obj
<<
  /Type /Page
  /Parent 2 0 R
  /MediaBox [ 0 0 612 792 ]
  /Resources <<
    /Font <<
      /F1 5 0 R
    >>
  >>
  /Annots [ ###FIELD_LIST### ]
>>
endobj

5 0 obj
<<
  /Type /Font
  /Subtype /Type1
  /BaseFont /Helvetica
  /Encoding /WinAnsiEncoding
>>
endobj

###FIELDS###

trailer
<<
  /Root 1 0 R
>>
%%EOF
"""

CHESS_BUTTON_TEMPLATE = r"""
###IDX### 0 obj
<<
  /Type /Annot
  /Subtype /Widget
  /FT /Btn
  /Ff 65536
  /T (B_###X###_###Y###)
  /DA (/F1 14 Tf 0 0 0 rg)
  /F 4
  /P 3 0 R
  /Rect [ ###RECT### ]
  /MK <<
    /BG [ ###BG_COLOR### ]
    /BC [ 0 0 0 ]
    /CA (###LABEL###)
  >>
  /A <<
    /S /JavaScript
    /JS (squareClicked(###X###, ###Y###);)
  >>
>>
endobj
"""

GRID_SIZE = 40
BOARD_OFFSET_X = 100
BOARD_OFFSET_Y = 600

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
    obj_idx_ctr = 10

    for y in range(8):
        for x in range(8):
            button = CHESS_BUTTON_TEMPLATE
            button = button.replace("###IDX###", str(obj_idx_ctr))
            label = initial_board[y][x] if initial_board[y][x] else " "
            button = button.replace("###LABEL###", label)
            bg_color = "1 1 1" if (x + y) % 2 == 0 else "0.8 0.8 0.8"
            button = button.replace("###BG_COLOR###", bg_color)
            
            llx = BOARD_OFFSET_X + x * GRID_SIZE
            lly = BOARD_OFFSET_Y - (y + 1) * GRID_SIZE
            urx = llx + GRID_SIZE
            ury = lly + GRID_SIZE
            button = button.replace("###RECT###", f"{llx} {lly} {urx} {ury}")
            
            button = button.replace("###X###", str(x))
            button = button.replace("###Y###", str(y))
            
            fields_text += button
            field_indexes.append(f"{obj_idx_ctr} 0 R")
            obj_idx_ctr += 1

    filled_pdf = CHESS_PDF_TEMPLATE.replace("###FIELDS###", fields_text)
    filled_pdf = filled_pdf.replace("###FIELD_LIST###", " ".join(field_indexes))
    
    with open("chess_game.pdf", "w", encoding="utf-8") as pdf_file:
        pdf_file.write(filled_pdf)

if __name__ == '__main__':
    generate_chess_pdf()