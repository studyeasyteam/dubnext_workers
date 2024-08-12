FROM quay.io/keycloak/keycloak:22.0

# Set build arguments for the Keycloak admin user and password
ARG KEYCLOAK_ADMIN
ARG KEYCLOAK_ADMIN_PASSWORD

# Set environment variables for Keycloak
ENV KEYCLOAK_ADMIN=admin
ENV KEYCLOAK_ADMIN_PASSWORD=admin123
ENV KEYCLOAK_LOGLEVEL=INFO
ENV ROOT_LOGLEVEL=INFO


# Set the working directory inside the container
WORKDIR /opt/keycloak

# Copy the necessary files and directories into the container
COPY ./compose/keycloak/realm-config /opt/keycloak/data/import


# Expose the Keycloak server port
# Note: We assume that KEYCLOAK_SERVER_PORT is passed as a build argument or environment variable during the build process.
EXPOSE ${KEYCLOAK_SERVER_PORT} 8081 8443

#Start Keycloak using the desired command
# Note: We assume that KEYCLOAK_DATABASE_URL, KEYCLOAK_DATABASE_USERNAME, and KEYCLOAK_DATABASE_PASSWORD
# are passed as build arguments or environment variables during the build process.
CMD ["start-dev", "--import-realm", "--db", "postgres", "--db-url-host", "${KEYCLOAK_DATABASE_URL}", "--db-username", "${KEYCLOAK_DATABASE_USERNAME}", "--db-password", "${KEYCLOAK_DATABASE_PASSWORD}"]

