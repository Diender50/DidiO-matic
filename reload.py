import main

while True:
    if is_changed(main):
        main = reload(main)
        
