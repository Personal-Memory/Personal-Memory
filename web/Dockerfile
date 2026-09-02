FROM node:22-alpine

WORKDIR /app
# the above line sets the working directory for the container to /app. Any subsequent commands will be run from this directory.
# naming the working directory is important because it allows you to organize your files and dependencies in a specific location within the container.
# there is another container that has a similar working directory. Is that a problem? No, it is not a problem. Each container has its own isolated filesystem, so the working directory in one container does not affect the working directory in another container.

COPY package*.json ./
# the above line copies the package.json and package-lock.json files from the host machine to the working directory in the container. These files contain information about the project's dependencies and scripts.

RUN npm install

COPY . .
# the above line copies all the files from the host machine to the working directory in the container. This includes the source code, configuration files, and any other necessary files for the application to run.
# so why did we have to copy the package.json and package-lock.json files separately before running npm install? This is because we want to take advantage of Docker's caching mechanism. By copying the package files first and running npm install, we can cache the installed dependencies. If the package files haven't changed, Docker will use the cached layer for npm install, which speeds up the build process. If we copied all the files at once, any change in the source code would invalidate the cache and require reinstalling dependencies, even if they haven't changed.
# so the pre copying is essential if we are changing the source code frequently but not the dependencies. This way, we can avoid unnecessary reinstallation of dependencies and speed up the build process.

EXPOSE 5173
# the above line exposes port 5173 from the container to the host machine. This allows you to access the application running in the container from your local machine.
# other containers can also access this port if they are on the same network. This is important for communication between containers in a multi-container setup.

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
# why is the --host 0.0.0.0 important? By default, the development server binds to localhost (127.0.0.1), which means it will only be accessible from within the container itself. By specifying 0.0.0.0, we tell the server to bind to all available network interfaces, making it accessible from outside the container as well.
# what is special about the zeros? The zeros in 0.0.0.0 represent the wildcard address, which means the server will listen on all available network interfaces.