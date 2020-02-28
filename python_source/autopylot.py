#  AutoLisp Commands for manipulation of parametric drawing
#  Adam Lee
#  October 2015
#  __________________________________________________________________

drawingtemplate = "drawing_template.dwg"
drawingoutput   = "new_drawing.dwg"

script = open('cad.scr', 'w')

# Switch off file dialogue boxes in CAD.
script.write(r'_filedia 0' '\n')

# If bricscad, switch off the command dialogue box 
# script.write(r'_cmddia off' '\n')
#  If autocad, switch off the command diaglogue box
script.write(r'_cmddia 0' '\n')

# Open a CAD file for editing.
script.write(r'_open ' + str(drawingtemplate) + '\n')

# Find the entity name assigned to an object with EDATA label "Side"
# for application AUTOPYLOT
script.write(r'''(setq autovar (ssget "X" '((1000 . "''')
script.write("Side")
script.write(r'''") (-3 ("AUTOPYLOT")))))''' '\n')

script.write(r'''(command "_ddedit" autovar "200.0" "")''')


script.write(r'''(setq autovar (ssget "X" '((1000 . "''')
script.write("Longside")
script.write(r'''") (-3 ("AUTOPYLOT")))))''' '\n')

script.write(r'''(command "_ddedit" autovar "500.0" "")''')


# Modify Text
script.write(r'''(setq autovar (ssget "X" '((1000 . "''')
script.write("TestText")
script.write(r'''") (-3 ("AUTOPYLOT")))))''' '\n')

script.write(r'''(entmod (subst '(1 . "New message") (assoc 1 (setq e (entget (ssname autovar 0)))) e))''' '\n')

# Update fields.
script.write(r'_updatefield all  commandline' '\n')

# Remove geometric and dimensional constraints.
script.write(r'_delconstraint all  commandline' '\n')

# Allegedly purge command should be run multiple # times.
script.write(r'_-purge all * no' '\n')
script.write(r'_-purge all * no' '\n')
script.write(r'_-purge all * no' '\n')

# Audit in model space, then audit in paperspace
script.write(r'_tilemode 1' '\n')
script.write(r'_audit yes'  '\n')
script.write(r'_tilemode 0' '\n')
script.write(r'_audit yes'  '\n')

# Tidy up and save drawing
script.write(r'_zoom extents' '\n')
script.write(r'_saveas 2010 ' + drawingoutput + '\n')
# script.write(r'_quit' '\n')


# Close files, shutown ########################################### {{{

script.close()

quit(0)

# End close files, run LaTeX, shutdown. ########################## }}}

# Old Stuff That Just Might Be Useful In The Future {{{

# script.write(r'''(if (> (sslength autovar) 1)''' '\n')
# script.write(r'''(*error* "Error. More than one entity named ''')
# script.write("Side")
# script.write(r'''")''' '\n')
# script.write(r'''(command "_quit")''' '\n')
# script.write(r''')''' '\n')
# script.write(r'''(if (< (sslength autovar) 1)''' '\n')
# script.write(r'''(*error* "Error. No entity named ''')
# script.write("Side")
# script.write(r'''")''' '\n')
# script.write(r'''(command "_quit")''' '\n')
# script.write(r''')''' '\n')


# For Bricscad: -
# script.write << "_ed (handent \"" << handle[i] << "\") " 
# In Bricscad the four lines below change parametric lengths in the
# drawing database, but they do not cause the shape of the drawing to
# update. 
# script.write(r'(setq en (ssname autovar 0))' '\n')
# script.write(r'(setq ed (entget en))' '\n') 
# script.write(r'(setq ed (subst (cons 1 "' + 'd1' + r'=' + '100' + r'") (assoc 1 ed) ed))' '\n')
# script.write(r'(entmod ed)' '\n')

# The script file below is a variant of the one above, causing the
# lengths of multiple Bricscad entities to be modified, but without
# causing the shape to update. 
# _filedia 0
# _cmddia 0
# _open drawing_template.dwg
# (setq autovar (ssget "X" '((1000 . "Side") (-3 ("AUTOPYLOT")))))
# (repeat (setq i (sslength autovar))
#     (setq en (ssname autovar (setq i (1- i))))
#     (setq ed (entget en))
#     (setq ed (subst (cons 1 "d1=100") (assoc 1 ed) ed))
#     (entmod ed)
#     (setq ed (entget en))
#     (setq ed (subst (cons 42 100) (assoc 42 ed) ed))
#     (entmod ed)
# )

# }}} End of old stuff that might be useful in the future.
