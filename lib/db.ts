import mysql from "mysql2/promise";
import type { QueryResult } from "@/types";

// Database connection configuration
const dbConfig = {
  host: process.env.DB_HOST || "localhost",
  port: Number(process.env.DB_PORT || "3306"),
  user: process.env.DB_USER || "care_connect_user",
  password: process.env.DB_PASSWORD || "Admin123",
  database: process.env.DB_NAME || "care_connect",
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
  connectTimeout: 10000, // 10 seconds
  enableKeepAlive: true,
  keepAliveInitialDelay: 10000, // 10 seconds
};

// Create a connection pool
const pool = mysql.createPool(dbConfig);

// Helper function to execute SQL queries
export async function query(
  sql: string,
  params: unknown[] = []
): Promise<QueryResult> {
  try {
    const [results] = await pool.execute(sql, params);
    return results as QueryResult;
  } catch (error) {
    console.error("Database query error:", error);
    throw error;
  }
}

// Initialize database connection with retry logic
export async function testConnection(
  retries = 5,
  delay = 2000
): Promise<boolean> {
  let currentTry = 0;

  while (currentTry < retries) {
    try {
      const connection = await pool.getConnection();
      console.log("Database connection successful");
      connection.release();
      return true;
    } catch (error) {
      currentTry++;
      console.error(
        `Database connection failed (attempt ${currentTry}/${retries}):`,
        error
      );

      if (currentTry >= retries) {
        console.error(
          "Maximum connection attempts reached. Could not connect to database."
        );
        return false;
      }

      console.log(`Retrying in ${delay / 1000} seconds...`);
      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }

  return false;
}
