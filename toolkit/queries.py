def query_users_trend():
    """Return the total number of newly-created user accounts in Synapse for each year."""

    return """
    WITH yearly_new_users AS (
        SELECT
            year(change_timestamp) AS query_year,
            count(DISTINCT id) AS yearly_new_users
        FROM 
            synapse_data_warehouse.synapse.userprofile_latest
        WHERE
            change_type = 'CREATE'
        GROUP BY
            year(change_timestamp)
    )
    SELECT
        query_year,
        sum(yearly_new_users) OVER (ORDER BY query_year) AS CUMULATIVE_USERS
    FROM
        yearly_new_users
    ORDER BY
        query_year DESC;
    """