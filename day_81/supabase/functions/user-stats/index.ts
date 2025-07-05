import { UserStatsResponse } from '../types.ts'
import { getUserStreak, getUserTotalCompletions, checkTodayCompletion } from '../utils/streak-utils.ts'

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
};

Deno.serve(async (req: Request) => {
  try {
    if (req.method === "OPTIONS") {
      return new Response(null, {
        status: 200,
        headers: corsHeaders,
      });
    }

    if (req.method !== "GET") {
      return new Response(
        JSON.stringify({ error: "Method not allowed" }),
        {
          status: 405,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        }
      );
    }

    // Import Supabase client
    const { createClient } = await import("npm:@supabase/supabase-js@2");
    
    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const supabaseServiceKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
    
    const supabase = createClient(supabaseUrl, supabaseServiceKey);

    const url = new URL(req.url);
    const userId = url.searchParams.get("user_id");

    if (!userId) {
      return new Response(
        JSON.stringify({ error: "Missing user_id parameter" }),
        {
          status: 400,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        }
      );
    }

    // Get all user stats in parallel
    const [streak, totalCompletions, completedToday, earnedBadges] = await Promise.all([
      getUserStreak(supabase, userId),
      getUserTotalCompletions(supabase, userId),
      checkTodayCompletion(supabase, userId),
      getEarnedBadgesCount(supabase, userId)
    ]);

    const response: UserStatsResponse = {
      stats: {
        currentStreak: streak?.current_streak || 0,
        longestStreak: streak?.longest_streak || 0,
        totalCompletions,
        earnedBadges,
        completedToday,
        lastCompletionDate: streak?.last_completion_date || null,
      }
    };

    return new Response(
      JSON.stringify(response),
      {
        status: 200,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      }
    );
  } catch (error) {
    console.error("Error in user-stats function:", error);
    return new Response(
      JSON.stringify({ 
        error: "Internal server error",
        details: error instanceof Error ? error.message : "Unknown error"
      }),
      {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      }
    );
  }
});

// Helper function to get earned badges count
async function getEarnedBadgesCount(supabase: any, userId: string): Promise<number> {
  const { count, error } = await supabase
    .from("user_badges")
    .select("*", { count: "exact", head: true })
    .eq("user_id", userId);

  if (error) {
    console.error("Error counting user badges:", error);
    return 0;
  }

  return count || 0;
}