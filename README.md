# WiFi PhoneSploit Auto-Targeter Makefile
# For authorized pentesting only

.PHONY: all install deps clean run scan test update-phonesploit help

# Default target
all: install run

# Installation and setup
install: deps phonesploit
	@echo "[+] Installation complete! Run 'make run' to start"

# Install Python dependencies
deps:
	@echo "[+] Installing Python dependencies..."
	pip3 install -r requirements.txt
	@echo "[+] Dependencies installed"

# Clone/setup PhoneSploit-Pro
phonesploit:
	@echo "[+] Setting up PhoneSploit-Pro..."
	@if [ ! -d "PhoneSploit-Pro" ]; then \
		git clone https://github.com/MasterDevX/PhoneSploit-Pro.git; \
		cd PhoneSploit-Pro && pip3 install -r requirements.txt; \
		echo "python3 ./PhoneSploit-Pro/phonesploit.py --help" > phonesploit_pro_test.py; \
		echo "[+] PhoneSploit-Pro installed successfully"; \
	else \
		echo "[+] PhoneSploit-Pro already exists"; \
	fi

# Create requirements.txt if it doesn't exist
requirements.txt:
	@echo "netifaces>=0.11.0" > requirements.txt
	@echo "argparse" >> requirements.txt

# Run the main tool
run: requirements.txt
	@echo "[+] Starting WiFi PhoneSploit Auto-Targeter..."
	@chmod +x wifitarget.py 2>/dev/null || true
	python3 wifitarget.py

# Quick network scan only
scan:
	@echo "[+] Running network scan only..."
	python3 wifitarget.py --manual

# Test PhoneSploit-Pro integration
test:
	@echo "[+] Testing PhoneSploit-Pro..."
	@if [ -f "PhoneSploit-Pro/phonesploit.py" ]; then \
		python3 PhoneSploit-Pro/phonesploit.py --help; \
		echo "[+] PhoneSploit-Pro test passed"; \
	else \
		echo "[-] PhoneSploit-Pro not found. Run 'make phonesploit' first"; \
		exit 1; \
	fi

# Update PhoneSploit-Pro
update-phonesploit:
	@echo "[+] Updating PhoneSploit-Pro..."
	cd PhoneSploit-Pro && git pull && pip3 install -r requirements.txt
	@echo "[+] PhoneSploit-Pro updated"

# Clean everything
clean:
	@echo "[+] Cleaning up..."
	rm -f requirements.txt *.pyc __pycache__/*
	rm -rf PhoneSploit-Pro/.git
	@echo "[+] Clean complete"

# Full fresh install
fresh:
	@echo "[+] Fresh install..."
	make clean
	make install

# Development mode with auto-reload
dev:
	@echo "[+] Starting in development mode..."
	while true; do \
		python3 wifitarget.py; \
		echo "[+] Restarting in 3 seconds... (Ctrl+C to stop)"; \
		sleep 3; \
	done

# Generate documentation
docs:
	@echo "[+] Generating documentation..."
	pydoc3 -w wifitarget.py
	@echo "[+] Documentation saved to wifitarget.html"

# Show help
help:
	@echo "WiFi PhoneSploit Auto-Targeter - Makefile Targets"
	@echo "================================================"
	@echo "make all              - Install deps + run (default)"
	@echo "make install          - Full setup (deps + PhoneSploit-Pro)"
	@echo "make deps             - Install Python requirements only"
	@echo "make phonesploit      - Setup PhoneSploit-Pro only"
	@echo "make run              - Run the main tool"
	@echo "make scan             - Run network scan only"
	@echo "make test             - Test PhoneSploit-Pro integration"
	@echo "make update-phonesploit - Update PhoneSploit-Pro"
	@echo "make dev              - Development mode with auto-reload"
	@echo "make fresh            - Clean + full fresh install"
	@echo "make clean            - Remove generated files"
	@echo "make docs             - Generate Python docs"
	@echo "make help             - Show this help"

# Save this as a note for your pentest methodology
note:
	@echo "Creating pentest methodology note..."
	@printf "%% Makefile targets for WiFi PhoneSploit Auto-Targeter\n" > note.txt
	@printf "%% Quick setup: make install\n" >> note.txt
	@printf "%% Quick run: make run\n" >> note.txt
	@cat note.txt