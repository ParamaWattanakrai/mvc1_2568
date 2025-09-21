import model
from view import App
from controller import Controller

if __name__ == '__main__':
    app_view = App()

    app_controller = Controller(model, app_view)

    app_view.set_controller(app_controller)

    app_controller.start()
    app_view.mainloop()