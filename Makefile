bundle:
	pyinstaller --nowindow --onefile --icon=icon.icns --osx-bundle-identifier=com.nicluo.speedrunner  SpeedRunner.spec

clean:
	$(RM) -r build dist
