#!/bin/sh

# Set the password for the elastic user
export ELASTIC_PASSWORD="elastic"
export ELASTIC_PORT="9200"
export ELASTIC_NODE_PORT="9300"
export ELASTIC_VERSION="8.13.0"
export KIBANA_PORT="5601"


setup_elasticsearch() {
    # Check if the elastic network already exists
    if ! docker network inspect elastic &>/dev/null; then
        # Create Docker network
        docker network create elastic
    fi

    # Check if the Elasticsearch image exists
    if ! docker image inspect docker.elastic.co/elasticsearch/elasticsearch:${ELASTIC_VERSION} &>/dev/null; then
        # Pull Elasticsearch image
        docker pull docker.elastic.co/elasticsearch/elasticsearch:${ELASTIC_VERSION}
    fi
}

start_elasticsearch() {
    # TODO: Check to see if the network is already set up, and the image exists. Otherwise, set up the network and pull the image
    # TODO: Check to see if ES is already running. If not, start ES.
    # Start ES
    # Check to see if ES is already running
    if docker ps -a --format '{{.Names}}' | grep -q "^es01$"; then
        echo "Elasticsearch is already running."
    else
        # Start ES and capture the output
        # TODO: Test this out
        docker run -d --name es01 --net elastic -p ${ELASTIC_PORT}:9200 -p ${ELASTIC_NODE_PORT}:9300 -e "discovery.type=single-node" -e "ELASTIC_PASSWORD=${ELASTIC_PASSWORD}" -t docker.elastic.co/elasticsearch/elasticsearch:${ELASTIC_VERSION}
    fi

    # Check if the CA certificate is already set up
    if [ ! -f http_ca.crt ]; then
        # Copy the CA certificate from the container to the host
        copy_ca_certificate
    fi
}


copy_ca_certificate() {
    retries=0
    max_retries=5
    backoff=1

    # Loop until the file is successfully copied or maximum retries are reached
    while [ $retries -lt $max_retries ]; do
        if [ -f http_ca.crt ]; then
            echo "CA certificate already copied."
            return
        fi

        # Attempt to copy the CA certificate from the container to the host
        docker cp es01:/usr/share/elasticsearch/config/certs/http_ca.crt . && return

        # Increment retry counter and apply exponential backoff
        ((retries++))
        sleep $backoff
        ((backoff *= 2))
    done

    echo "Failed to copy CA certificate after $max_retries attempts."
}

check_elasticsearch_status() {
    # Check if ES is already running
    if ! docker ps -a --format '{{.Names}}' | grep -q "^es01$" ; then
        echo "Elasticsearch is not running."
        exit 1
    else
        # Check ES status
        curl --cacert http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:${ELASTIC_PORT}
    fi
}

stop_elasticsearch() {
    # Check if ES is running
    if docker ps -a --format '{{.Names}}' | grep -q "^es01$"; then
        # Stop ES
        docker stop es01
        echo "Elasticsearch stopped."
    else
        echo "Elasticsearch is not running."
    fi
}

remove_elasticsearch() {
    # Check if ES container exists
    if docker ps -a --format '{{.Names}}' | grep -q "^es01$"; then
        # Stop ES container
        docker stop es01
        # Remove ES container
        docker rm es01
        echo "Elasticsearch container removed."
    else
        echo "Elasticsearch container does not exist."
    fi

    # Check if elastic network exists
    if docker network inspect elastic &>/dev/null; then
        # Remove elastic network
        docker network rm elastic
        echo "Elasticsearch network removed."
    else
        echo "Elasticsearch network does not exist."
    fi

    # Check if http_ca.crt file exists
    if [ -f http_ca.crt ]; then
        # Remove http_ca.crt file
        rm http_ca.crt
        echo "http_ca.crt file removed."
    else
        echo "http_ca.crt file does not exist."
    fi
}

start_kibana() {
    # Pull Kibana image
    if ! docker image inspect docker.elastic.co/kibana/kibana:${ELASTIC_VERSION} &>/dev/null; then
        docker pull docker.elastic.co/kibana/kibana:${ELASTIC_VERSION}
    fi

    # Check if Kibana is already running
    if docker ps -a --format '{{.Names}}' | grep -q "^kibana$"; then
        echo "Kibana is already running."
    else
        # Start Kibana
        docker run -d --name kibana --net elastic -p ${KIBANA_PORT}:5601 docker.elastic.co/kibana/kibana:${ELASTIC_VERSION}
    fi
    # When you start Kibana, a unique URL is output to your terminal. To access Kibana:
    # - Open the generated URL in your browser.
    # - Paste the enrollment token that you copied earlier, to connect your Kibana instance with Elasticsearch.
    # - Log in to Kibana as the elastic user with the password that was generated when you started Elasticsearch.
}

stop_kibana() {
    # Check if Kibana is running
    if docker ps -a --format '{{.Names}}' | grep -q "^kibana$"; then
        # Stop Kibana
        docker stop kibana
        echo "Kibana stopped."
    else
        echo "Kibana is not running."
    fi
}

remove_kibana() {
    # Check if Kibana container exists
    if docker ps -a --format '{{.Names}}' | grep -q "^kibana$"; then
        # Stop Kibana container
        docker stop kibana
        # Remove Kibana container
        docker rm kibana
        echo "Kibana container removed."
    else
        echo "Kibana container does not exist."
    fi
}

remove_all() {
    # Remove Elasticsearch
    remove_elasticsearch

    # Remove Kibana
    remove_kibana
}

# Main function to handle command-line arguments
main() {
    # Check if no arguments provided
    if [ $# -eq 0 ]; then
        echo "Usage: $0 [--setup-es --start-es --stop-es --remove-es --start-kibana --stop-kibana --remove-kibana --remove-all]"
        exit 1
    fi

    # Parse command-line arguments
    while [[ $# -gt 0 ]]; do
        key="$1"

        case $key in
            --setup-es)
                setup_elasticsearch
                exit 0
                ;;
            --start-es)
                start_elasticsearch
                check_elasticsearch_status
                exit 0
                ;;
            --stop-es)
                stop_elasticsearch
                exit 0
                ;;
            --remove-es)
                remove_elasticsearch
                exit 0
                ;;
            --start-kibana)
                start_kibana
                exit 0
                ;;
            --stop-kibana)
                stop_kibana
                exit 0
                ;;
            --remove-kibana)
                remove_kibana
                exit 0
                ;;
            --remove-all)
                remove_all
                exit 0
                ;;
            --elastic-port)
                export ELASTIC_PORT="$2"
                shift
                ;;
            --elastic-node-port)
                export ELASTIC_NODE_PORT="$2"
                shift
                ;;
            --elastic-version)
                export ELASTIC_VERSION="$2"
                shift
                ;;
            --kibana-port)
                export KIBANA_PORT="$2"
                shift
                ;;
            *)
                echo "Invalid option: $key"
                echo "Usage: $0 [--setup-es --start-es --stop-es --remove-es --start-kibana --stop-kibana --remove-kibana --remove-all]"
                exit 1
                ;;
        esac
        shift
    done
}

# Call the main function with command-line arguments
main "$@"
