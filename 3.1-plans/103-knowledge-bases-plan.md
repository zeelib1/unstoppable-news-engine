# Implementation Plan: Knowledge Bases Migration & Model

**Issue:** #103  
**Title:** [BACKEND] Create knowledge_bases migration & model  
**Assigned:** 2026-01-28 16:15 CET  
**Estimated Time:** 15-20 minutes

---

## Overview

Create the foundational database structure for storing knowledge base metadata in AskFiles. Each knowledge base represents a collection of uploaded documents that have been processed and embedded for semantic search. This is the first data model in the system and will be referenced by document chunks and search operations.

---

## Files to Create/Modify

### New Files
1. `api/database/migrations/YYYY_MM_DD_HHMMSS_create_knowledge_bases_table.php`
   - Database migration for knowledge_bases table

2. `api/app/Models/KnowledgeBase.php`
   - Eloquent model for knowledge bases

3. `api/tests/Unit/Models/KnowledgeBaseTest.php`
   - Unit tests for the model

### Files to Review (Context)
- `api/database/migrations/` - Check existing migration patterns
- `api/app/Models/User.php` - Review model conventions
- `api/config/database.php` - Confirm SQLite configuration

---

## Implementation Steps

### Step 1: Create Migration File
**File:** `api/database/migrations/YYYY_MM_DD_HHMMSS_create_knowledge_bases_table.php`

**Action:**
```bash
cd api
php artisan make:migration create_knowledge_bases_table
```

**Migration Schema:**
```php
Schema::create('knowledge_bases', function (Blueprint $table) {
    $table->uuid('id')->primary();
    $table->string('title', 255);
    $table->string('slug', 255)->unique()->index();
    $table->integer('file_count')->default(0);
    $table->integer('chunk_count')->default(0);
    $table->timestamps();
});
```

**Why:**
- **UUID primary key:** Prevents enumeration attacks, globally unique identifiers
- **title:** Human-readable name for the knowledge base
- **slug:** URL-friendly identifier for sharing (e.g., `askfiles.io/kb/my-project-docs`)
- **file_count:** Track number of files uploaded (for UI display)
- **chunk_count:** Track number of text chunks embedded (for stats)
- **timestamps:** created_at/updated_at for auditing

**Risk:** Low  
**Dependencies:** None

---

### Step 2: Create Eloquent Model
**File:** `api/app/Models/KnowledgeBase.php`

**Action:**
```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Concerns\HasUuids;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Str;

class KnowledgeBase extends Model
{
    use HasFactory, HasUuids;

    protected $fillable = [
        'title',
        'slug',
    ];

    protected $casts = [
        'file_count' => 'integer',
        'chunk_count' => 'integer',
    ];

    protected static function boot()
    {
        parent::boot();

        static::creating(function ($knowledgeBase) {
            if (empty($knowledgeBase->slug)) {
                $knowledgeBase->slug = Str::slug($knowledgeBase->title);
                
                // Ensure uniqueness
                $originalSlug = $knowledgeBase->slug;
                $counter = 1;
                while (static::where('slug', $knowledgeBase->slug)->exists()) {
                    $knowledgeBase->slug = $originalSlug . '-' . $counter++;
                }
            }
        });
    }
}
```

**Why:**
- **HasUuids trait:** Auto-generates UUID for id field (Laravel 11 feature)
- **HasFactory trait:** Enables model factories for testing
- **fillable:** Allows mass assignment of title and slug
- **casts:** Type-cast integers for consistent API responses
- **boot() method:** Auto-generate unique slug from title on creation

**Risk:** Low  
**Dependencies:** Requires Step 1 (migration must exist)

---

### Step 3: Write Unit Tests
**File:** `api/tests/Unit/Models/KnowledgeBaseTest.php`

**Action:**
```php
<?php

namespace Tests\Unit\Models;

use App\Models\KnowledgeBase;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class KnowledgeBaseTest extends TestCase
{
    use RefreshDatabase;

    public function test_it_creates_knowledge_base_with_uuid(): void
    {
        $kb = KnowledgeBase::create(['title' => 'Test KB']);

        $this->assertInstanceOf(KnowledgeBase::class, $kb);
        $this->assertIsString($kb->id);
        $this->assertMatchesRegularExpression('/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i', $kb->id);
    }

    public function test_it_auto_generates_slug_from_title(): void
    {
        $kb = KnowledgeBase::create(['title' => 'My Test Knowledge Base']);

        $this->assertEquals('my-test-knowledge-base', $kb->slug);
    }

    public function test_it_ensures_slug_uniqueness(): void
    {
        KnowledgeBase::create(['title' => 'Duplicate']);
        $kb2 = KnowledgeBase::create(['title' => 'Duplicate']);

        $this->assertEquals('duplicate', KnowledgeBase::first()->slug);
        $this->assertEquals('duplicate-1', $kb2->slug);
    }

    public function test_it_has_default_counts(): void
    {
        $kb = KnowledgeBase::create(['title' => 'Test']);

        $this->assertEquals(0, $kb->file_count);
        $this->assertEquals(0, $kb->chunk_count);
    }

    public function test_it_casts_counts_to_integers(): void
    {
        $kb = KnowledgeBase::create(['title' => 'Test']);
        
        $this->assertIsInt($kb->file_count);
        $this->assertIsInt($kb->chunk_count);
    }
}
```

**Why:**
- Tests UUID generation
- Tests slug auto-generation
- Tests slug uniqueness constraint
- Tests default values
- Tests type casting

**Risk:** Low  
**Dependencies:** Requires Step 1 & 2 (migration + model)

---

### Step 4: Run Migration
**Action:**
```bash
cd api
php artisan migrate
```

**Verify:**
```bash
php artisan db:show
# Should show knowledge_bases table

sqlite3 database/database.sqlite ".schema knowledge_bases"
# Should show table structure
```

**Why:** Apply the migration to create the actual table

**Risk:** Low  
**Dependencies:** Requires Step 1

---

### Step 5: Run Tests
**Action:**
```bash
cd api
./vendor/bin/phpunit tests/Unit/Models/KnowledgeBaseTest.php
```

**Expected Output:**
```
PHPUnit 11.5.3 by Sebastian Bergmann and contributors.

.....                                                               5 / 5 (100%)

Time: 00:00.123, Memory: 24.00 MB

OK (5 tests, 10 assertions)
```

**Why:** Verify everything works before committing

**Risk:** Low  
**Dependencies:** Requires Steps 1-4

---

## Testing Strategy

### Unit Tests (Step 3)
- Model creation
- UUID generation
- Slug auto-generation
- Slug uniqueness
- Default values
- Type casting

**Target Coverage:** 100% (simple model, should be easy)

### Database Tests
- Migration runs without errors
- Migration rollback works
- Table schema matches expectations

### Integration Tests (Future)
- Will be tested in #107 (Upload Endpoint) when creating knowledge bases via API

---

## Acceptance Criteria

- [x] Migration file exists
- [ ] Migration creates table with correct schema
- [ ] Migration is reversible (rollback works)
- [x] Model file exists with HasUuids trait
- [ ] Model auto-generates slugs from title
- [ ] Slugs are unique (duplicate titles get -1, -2, etc.)
- [ ] Default values applied (file_count = 0, chunk_count = 0)
- [x] Unit tests file exists
- [ ] All 5 unit tests pass
- [ ] Test coverage ≥ 80% (targeting 100%)
- [ ] Code formatted (php-cs-fixer)
- [ ] No PHPStan errors

---

## Potential Issues & Mitigations

### Issue 1: Slug Collision
**Problem:** Two knowledge bases with same title created simultaneously  
**Mitigation:** Use database transaction in creating() hook  
**Likelihood:** Very low (single-user during MVP)

### Issue 2: UUID Collision
**Problem:** UUID generation conflicts  
**Mitigation:** Laravel's HasUuids uses ramsey/uuid (cryptographically random)  
**Likelihood:** Negligible (1 in 2^122)

### Issue 3: Migration Fails
**Problem:** SQLite connection issues  
**Mitigation:** Verify database.sqlite file exists, check permissions  
**Likelihood:** Low (file already exists from Laravel install)

---

## Dependencies

**No dependencies** - This is the first data model, foundation for:
- Issue #104: document_chunks (will reference knowledge_bases via foreign key)
- Issue #107: Upload endpoint (will create knowledge bases)
- Issue #108: Search endpoint (will query by knowledge base)

---

## Time Breakdown

| Task | Estimated Time |
|------|----------------|
| Create migration | 3 min |
| Create model | 5 min |
| Write tests | 7 min |
| Run migration + tests | 2 min |
| Fix any issues | 3 min buffer |
| **Total** | **15-20 min** |

---

## Success Indicators

✅ **Green Test Suite**
```bash
./vendor/bin/phpunit tests/Unit/Models/KnowledgeBaseTest.php
# OK (5 tests, 10 assertions)
```

✅ **Migration Applied**
```bash
php artisan migrate:status
# knowledge_bases table listed
```

✅ **No Code Quality Issues**
```bash
./vendor/bin/php-cs-fixer fix --dry-run
# No files need fixing
```

✅ **Ready for Next Issue**
- #104 can now add foreign key to knowledge_bases
- #107 can create knowledge base records

---

## Next Steps

After this issue is complete:
1. **Issue #104:** Create document_chunks migration (will add foreign key to knowledge_bases)
2. **Issue #105:** Create OpenAI embeddings service (parallel, no dependency)
3. **Issue #106:** Create Qdrant integration service (parallel, no dependency)

---

**Status:** 📋 Plan Complete - Ready for Implementation  
**Reviewer:** Awaiting approval  
**Next Command:** `/tdd 103` (after approval)
