const main = ({
    float,
    integer,
    string,
}) => {
    const namespace = string('CI_PROJECT_NAME')
        .toLowerCase()
        .replace(/\./g, '-')
    const port = string('PORT', '8501')

    const config = {
        applications: [{
            container: {
                image: string('CONTAINER_IMAGE_SERVER'),
            },
            healthcheck: {
                path: '/healthz',
            },
            server: {
                port,
            },
            securityContext: {
                runAsUser: 0,
                runAsNonRoot: false,
                allowPrivilegeEscalation: true,
            },
        },],
        instances: integer('INSTANCES', 1),
        namespace,
    }
    return config
}

module.exports = main
