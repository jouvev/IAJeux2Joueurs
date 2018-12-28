JEU=Othello

all:
	cd $(JEU) && time python main.py

clean:
	find -type f -name "*.pyc" -a -exec rm -rf {} \;

.PHONY: all clean
