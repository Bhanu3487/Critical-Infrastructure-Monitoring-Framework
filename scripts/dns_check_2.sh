#!/bin/bash

# Check if hostname was provided
if [ -z "$1" ]; then
    echo "Usage: $0 <hostname>"
    exit 1
fi

HOST="$1"
echo "=== DNS Check for $HOST ==="

check_dns_record() {
    TYPE="$1"
    echo -e "\n[+] Querying $TYPE record for $HOST..."

    OUTPUT=$(dig "$HOST" "$TYPE" +nocomments +noquestion +stats +nocmd)
    FLAGS=$(echo "$OUTPUT" | grep "flags:")

    # Error checks
    if echo "$OUTPUT" | grep -q "status: NXDOMAIN"; then
        echo "[-] $TYPE record: NXDOMAIN (Non-Existent Domain)"
        return
    fi
    if echo "$OUTPUT" | grep -q "status: SERVFAIL"; then
        echo "[-] $TYPE record: SERVFAIL (Server Failure)"
        return
    fi
    if echo "$OUTPUT" | grep -q "status: REFUSED"; then
        echo "[-] $TYPE record: REFUSED (Query Refused)"
        return
    fi

    # Record data extraction
    RECORDS=$(echo "$OUTPUT" | grep -E "IN[[:space:]]+$TYPE" | awk '{print $NF}')
    if [ -z "$RECORDS" ]; then
        echo "[-] $TYPE record: No records found"
    else
        echo "[✓] $TYPE record returned:"
        echo "$RECORDS" | while read -r RECORD; do
            echo "    - $RECORD"
            # Additional check for A records pointing to private IPs
            if [[ "$TYPE" == "A" && "$RECORD" =~ ^(10\.|172\.(1[6-9]|2[0-9]|3[0-1])\.|192\.168\.) ]]; then
                echo "      [NOTE] Private/RFC1918 IP detected"
            fi
        done
    fi

    # Query metadata
    QTIME=$(echo "$OUTPUT" | grep "Query time:" | awk '{print $4}')
    echo "    -> Query time: $QTIME ms"

    # TTL analysis
    TTL=$(echo "$OUTPUT" | grep -E "IN[[:space:]]+$TYPE" | awk '{print $2}' | head -n1)
    echo "    -> TTL: ${TTL:-Not available} seconds"
    if [[ -n "$TTL" ]]; then
        if [[ "$TTL" -gt 86400 ]]; then
            echo "      [NOTE] Long TTL (>1 day) - changes will propagate slowly"
        elif [[ "$TTL" -lt 300 ]]; then
            echo "      [NOTE] Short TTL (<5 min) - allows quick DNS changes"
        fi
    fi

    # Nameserver info
    SERVER_LINE=$(echo "$OUTPUT" | grep -i "server:" | head -n1)
    SERVER_IP=$(echo "$SERVER_LINE" | grep -oE '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | head -n1)
    SERVER_PORT=$(echo "$SERVER_LINE" | grep -oE '#[0-9]+' | cut -d'#' -f2 | head -n1)
    
    if [ -n "$SERVER_IP" ]; then
        if [ -n "$SERVER_PORT" ]; then
            echo "    -> Nameserver: $SERVER_IP (port $SERVER_PORT)"
        else
            echo "    -> Nameserver: $SERVER_IP"
        fi
        # Check if we're using the authoritative NS
        if [[ "$HOST" == *"iitgn.ac.in" && "$SERVER_IP" != "10.0.136.7" ]]; then
            echo "      [WARNING] Not querying authoritative nameserver directly"
        fi
    fi

    # Authority check
    if echo "$FLAGS" | grep -q "aa"; then
        echo "    -> Authoritative: YES ✅"
    else
        echo "    -> Authoritative: NO (cached/recursive) ⚠"
    fi
}

# Main checks
check_dns_record "A"
check_dns_record "AAAA"
check_dns_record "MX"  # Added mail server check

# Special domain checks
if [[ "$HOST" == *"iitgn.ac.in" ]]; then
    echo -e "\n[+] Performing additional checks for iitgn.ac.in domain..."
    
    # NS records check with SOA verification
    echo -e "\n[+] Checking authoritative DNS configuration..."
    NS_RECORDS=$(dig "iitgn.ac.in" "NS" +short)
    SOA_RECORD=$(dig "iitgn.ac.in" "SOA" +short)
    
    if [ -z "$NS_RECORDS" ]; then
        echo "[-] No NS records found for iitgn.ac.in"
    else
        echo "[✓] Authoritative name servers:"
        echo "$NS_RECORDS" | while read -r NS; do
            echo "    - $NS"
        done
        
        echo -e "\n[+] SOA record:"
        if [ -z "$SOA_RECORD" ]; then
            echo "[-] No SOA record found"
        else
            echo "    - $SOA_RECORD"
        fi
        
        echo -e "\n[+] Nameserver verification:"
        echo "$NS_RECORDS" | while read -r NS; do
            echo "    - $NS:"
            IPV4=$(dig "$NS" "A" +short)
            IPV6=$(dig "$NS" "AAAA" +short)
            [ -n "$IPV4" ] && echo "      IPv4: $IPV4" || echo "      IPv4: None"
            [ -n "$IPV6" ] && echo "      IPv6: $IPV6" || echo "      IPv6: None"
            
            # Check if NS is responsive
            if dig "@$NS" "iitgn.ac.in" "SOA" +short >/dev/null 2>&1; then
                echo "      Status: Responding ✅"
            else
                echo "      Status: Not responding ❌"
            fi
        done
    fi
    
    # CNAME and reverse DNS checks
    echo -e "\n[+] Checking CNAME and PTR records..."
    CNAME_RECORD=$(dig "$HOST" "CNAME" +short)
    if [ -z "$CNAME_RECORD" ]; then
        echo "    - $HOST is not a CNAME alias"
    else
        echo "    - $HOST is an alias for: $CNAME_RECORD"
    fi
    
    # Check reverse DNS for all A records
    A_RECORDS=$(dig "$HOST" "A" +short)
    echo "    - Reverse DNS (PTR) checks:"
    if [ -z "$A_RECORDS" ]; then
        echo "      No A records found for PTR check"
    else
        echo "$A_RECORDS" | while read -r IP; do
            PTR=$(dig -x "$IP" +short)
            if [ -z "$PTR" ]; then
                echo "      $IP → No PTR record"
            else
                echo "      $IP → $PTR"
            fi
        done
    fi
fi

echo -e "\n=== DNS Check Completed ==="