import { CompleteRitualRequest, CompleteRitualResponse } from '../types.ts'
import { 
  getTodayDate, 
  calculateStreakUpdate, 
  updateUserStreak, 
  getUserStreak, 
  checkTodayCompletion 
} from '../utils/streak-utils.ts'
import { checkAndAwardBadges, getUserStatsForBadges } from '../utils/badge-utils.ts'

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

    if (req.method !== "POST") {
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

    const { user_id, ritual_id }: CompleteRitualRequest = await req.json();

    if (!user_id || !ritual_id) {
      return new Response(
        JSON.stringify({ error: "Missing user_id or ritual_id" }),
        {
          status: 400,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        }
      );
    }

    // Validate that the ritual exists
    const { data: ritual, error: ritualError } = await supabase
      .from("rituals")
      .select("id")
      .eq("id", ritual_id)
      .single();

    if (ritualError || !ritual) {
      return new Response(
        JSON.stringify({ error: "Invalid ritual_id" }),
        {
          status: 400,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        }
      );
    }

    // Check if already completed today
    const alreadyCompleted = await checkTodayCompletion(supabase, user_id);
    if (alreadyCompleted) {
      return new Response(
        JSON.stringify({ error: "Ritual already completed today" }),
        {
          status: 409,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        }
      );
    }

    const today = getTodayDate();

    // Insert completion
    const { data: completion, error: completionError } = await supabase
      .from("daily_completions")
      .insert([
        {
          user_id,
          ritual_id,
          date: today,
        },
      ])
      .select()
      .single();

    if (completionError) {
      console.error("Error inserting completion:", completionError);
      throw new Error("Failed to record completion");
    }

    // Get current user streak
    const currentStreak = await getUserStreak(supabase, user_id);

    // Calculate new streak
    const streakUpdate = calculateStreakUpdate(
      currentStreak?.last_completion_date || null,
      currentStreak?.current_streak || 0,
      currentStreak?.longest_streak || 0
    );

    // Update streak in database
    await updateUserStreak(supabase, user_id, streakUpdate);

    // Get user stats for badge checking
    const userStats = await getUserStatsForBadges(supabase, user_id);

    // Check and award badges
    const newBadges = await checkAndAwardBadges(supabase, user_id, userStats);

    const response: CompleteRitualResponse = {
      success: true,
      completion,
      newBadges,
      currentStreak: streakUpdate.currentStreak,
      longestStreak: streakUpdate.longestStreak
    };

    return new Response(
      JSON.stringify(response),
      {
        status: 200,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      }
    );
  } catch (error) {
    console.error("Error in complete-ritual function:", error);
    return new Response(
      JSON.stringify({ 
        success: false,
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