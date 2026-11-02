# MapNuke click helper for the dom6-ui guard. Source it:  . mapnuke_ui.sh ; mseq "X Y" ["X Y" ...]
# Unity misses a press that arrives with the pointer move, and an opening dropdown list ignores
# clicks while it fades in, so each click is: move, wait 800 ms, press 100 ms, wait 800 ms.
# All clicks of one call run in one dom6ui seq (the guard hands focus back to the terminal after
# each call). Coordinates are window pixels of the 1600x900 MapNuke window. Prints the final
# full-size screenshot path.
export UI_WMCLASS=MapNuke
U="$(dirname "${BASH_SOURCE[0]}")/../../dom6-ui/scripts/dom6ui.py"
mseq() { local s=(); for p in "$@"; do s+=("move $p" "wait 800" "click $p --hold 100" "wait 800"); done
         python3 -I "$U" seq "${s[@]}" "shot --full" | grep -o '/home[^ ]*png' | tail -1; }
