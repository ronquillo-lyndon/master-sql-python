-- Dataset 3-1: Dirty User Registration Log
DROP TABLE IF EXISTS raw_leads;

CREATE TABLE raw_leads (
    lead_id INT PRIMARY KEY,
    raw_name VARCHAR(100),
    raw_email VARCHAR(100),
    country VARCHAR(30)
);

INSERT INTO raw_leads (lead_id, raw_name, raw_email, country) VALUES
(1, '   ALEXANDER SMITH  ', 'ALEX@EXAMPLE.COM   ', 'USA'),
(2, 'maria garcia', '   Maria.Garcia@Domain.Org', 'spain'),
(3, '  KEVIN TRAN  ', 'kevin.tran@company.io', 'VIETNAM'),
(4, ' Sarah Connor ', '  SARAH.C@SKY.NET ', 'usa'),
(5, 'david  lee', 'DAVID.LEE@WEBMAIL.COM', 'Canada');
