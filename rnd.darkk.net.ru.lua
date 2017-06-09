-- uses PowerDNS recursor 4.x, does not work with 3.x

function getnum ( domain )
    domain = domain:lower()
    ttl, count = string.match(domain, '^(%d+)%.(%d+)%.rnd%.darkk%.net%.ru%.$')
    if ttl ~= nil then
        return tonumber(ttl), tonumber(count)
    end
    count = string.match(domain, '^(%d+)%.rnd%.darkk%.net%.ru%.$')
    if count ~= nil then
        return 60, tonumber(count)
    end
    return nil
end

function preresolve ( dq )
    if dq.qname:equal("myip.rnd.darkk.net.ru.") then
        if dq.qtype == pdns.A then
            dq.rcode = 0
            dq:addAnswer(pdns.A, dq.remoteaddr:toString(), 0)
        elseif dq.qtype == pdns.TXT then
            dq.rcode = 0
            dq:addAnswer(pdns.TXT, "\"Return IP address of client sending the query\"", 300)
        end
        return true
    elseif dq.qname:equal("rnd.darkk.net.ru.") and dq.qtype == pdns.TXT then
        dq.rcode = 0
        dq:addAnswer(pdns.TXT, "\"rnd.darkk.net.ru. is zone for testing OONI tools, don't abuse it\"", 300)
        return true
    else
        ttl, count = getnum(dq.qname:toString())
        if ttl ~= nil then
            if count > 4080 then -- 4093
                count = 4080
            end
            if dq.qtype == pdns.A then
                dq.rcode = 0
                for ndx = 1, count, 1 do
                    dq:addAnswer(pdns.A, string.format("%d.%d.%d.%d", math.random(0, 255), math.random(0, 255), math.random(0, 255), math.random(0, 255)), ttl)
                end
            elseif dq.qtype == pdns.TXT then
                dq.rcode = 0
                dq:addAnswer(pdns.TXT, "\"<ttl>.<count>.rnd.darkk.net.ru generates $count random A responses with $ttl TTL\"", 300)
            end
            return true
        end
    end
    dq.rcode = pdns.DROP
    return true
end

function nxdomain ( remoteip, domain, qtype )
    return false
end
