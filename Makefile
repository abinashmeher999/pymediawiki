TARGET:
	@if [ ! -d "venv" ]; then \
		printf "\033[1;31mVirtual environment not intialized, initializing...\033[0m\n"; \
		sudo pip install virtualenv; \
		virtualenv -p /usr/bin/python3 venv; \
	else echo "installed!"; \
	fi
	@printf "\033[1;31mActivate virtual environment with source venv/bin/activate command.\033[0m\n"
	@printf "\033[1;31mTo install dependencies, use pip install -r requirements.txt.\033[0m\n"
	@printf "\033[1;31mrun sample code wiki_cat.py using python3 wiki_cat.py.\033[0m\n"
	
uninstall:
	rm -R venv/

