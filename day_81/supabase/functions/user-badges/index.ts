import { UserBadgesResponse, BadgeWithProgress } from '../types.ts'
import { getUserStreak, getUserTotalCompletions } from '../utils/streak-utils.ts'
import { getAllBadges, getUserEarnedBadges } from '../utils/badge-utils.ts'

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

    // Get all data in parallel
    const [allBadges, userBadges, streak, totalCompletions] = await Promise.all([
      getAllBadges(supabase),
      getUserEarnedBadges(supabase, userId),
      getUserStreak(supabase, userId),
      getUserTotalCompletions(supabase, userId)
    ]);

    const earnedBadgeIds = new Set(userBadges);

    const badges: BadgeWithProgress[] = allBadges.map(badge => {
      const earned = earnedBadgeIds.has(badge.id);
      let progress = 0;
      let currentValue = 0;

      if (!earned) {
        const criteria = badge.criteria as any;
        if (criteria.type === 'completion') {
          currentValue = totalCompletions;
          progress = Math.min(100, (currentValue / criteria.value) * 100);
        } else if (criteria.type === 'streak') {
          currentValue = streak?.current_streak || 0;
          progress = Math.min(100, (currentValue / criteria.value) * 100);
        } else if (criteria.type === 'early_bird') {
          // Early bird logic would go here
          currentValue = 0;
          progress = 0;
        }
      }

      return {
        id: badge.id,
        name: badge.name,
        description: badge.description,
        icon: badge.icon,
        requirement: (badge.criteria as any).value,
        type: (badge.criteria as any).type,
        earned,
        progress,
        currentValue,
        earnedAt: earned ? userBadges.find(ub => ub === badge.id) : null,
      };
    });

    const earnedBadges = badges.filter(b => b.earned);
    const availableBadges = badges.filter(b => !b.earned);

    const response: UserBadgesResponse = {
      badges: {
        earned: earnedBadges,
        available: availableBadges,
        total: badges.length,
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
    console.error("Error in user-badges function:", error);
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