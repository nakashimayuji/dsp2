SELECT 
    id,
    store_name,
    business_type,
    address,
    prefecture,
    district,
    block,
    street,
    corporate_name,
    license_code,
    init_license_dt,
    license_expire_dt
FROM 
    "minato_restaurant"
WHERE 
    block = '南麻布四丁目' AND 
    business_type = '飲食店営業';