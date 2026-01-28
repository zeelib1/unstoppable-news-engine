# Issue #104: Document Chunks Migration & Model

**Created:** 2026-01-28 16:17 CET  
**Assignee:** Ralph (AI Agent)  
**Dependencies:** Issue #103 (Knowledge Bases)  
**Time Estimate:** 10-15 minutes  
**Complexity:** Low

---

## Issue Summary

Create the `document_chunks` table migration and Eloquent model to store text chunks extracted from uploaded documents. Each chunk will be embedded and stored in Qdrant for semantic search.

---

## Objectives

1. Create migration for `document_chunks` table
2. Create `DocumentChunk` Eloquent model
3. Define relationships with `KnowledgeBase` model
4. Write comprehensive tests
5. Validate 100% test coverage

---

## Database Schema

### Table: `document_chunks`

```sql
id                  bigint (PK)
knowledge_base_id   bigint (FK → knowledge_bases.id)
content             text (chunk text)
chunk_index         integer (position in document)
token_count         integer (approx tokens)
metadata            json (page, section, etc.)
qdrant_point_id     string (UUID in Qdrant)
created_at          timestamp
updated_at          timestamp
```

**Indexes:**
- `knowledge_base_id` (FK index)
- `qdrant_point_id` (for lookups)

---

## Files to Create

### 1. Migration
**Path:** `backend/database/migrations/YYYY_MM_DD_HHMMSS_create_document_chunks_table.php`

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('document_chunks', function (Blueprint $table) {
            $table->id();
            $table->foreignId('knowledge_base_id')
                  ->constrained('knowledge_bases')
                  ->onDelete('cascade');
            $table->text('content');
            $table->integer('chunk_index');
            $table->integer('token_count');
            $table->json('metadata')->nullable();
            $table->string('qdrant_point_id')->nullable()->unique();
            $table->timestamps();

            $table->index('knowledge_base_id');
            $table->index('qdrant_point_id');
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('document_chunks');
    }
};
```

---

### 2. Model
**Path:** `backend/app/Models/DocumentChunk.php`

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class DocumentChunk extends Model
{
    protected $fillable = [
        'knowledge_base_id',
        'content',
        'chunk_index',
        'token_count',
        'metadata',
        'qdrant_point_id',
    ];

    protected $casts = [
        'metadata' => 'array',
        'chunk_index' => 'integer',
        'token_count' => 'integer',
    ];

    public function knowledgeBase(): BelongsTo
    {
        return $this->belongsTo(KnowledgeBase::class);
    }
}
```

---

### 3. Update KnowledgeBase Model
**Path:** `backend/app/Models/KnowledgeBase.php`

**Add relationship:**
```php
public function chunks(): HasMany
{
    return $this->hasMany(DocumentChunk::class);
}
```

**Add to top:**
```php
use Illuminate\Database\Eloquent\Relations\HasMany;
```

---

### 4. Test File
**Path:** `backend/tests/Unit/Models/DocumentChunkTest.php`

**Tests to write:**
1. ✅ Can create document chunk
2. ✅ Can retrieve document chunk
3. ✅ Has knowledge_base relationship
4. ✅ Casts metadata as array
5. ✅ Can query chunks by knowledge_base_id
6. ✅ Cascade deletes when knowledge base is deleted

---

## Implementation Steps (TDD)

### Step 1: Write Tests (RED)
```bash
php artisan make:test Models/DocumentChunkTest --unit
```

Write all 6 test cases (they will fail initially)

---

### Step 2: Create Migration (GREEN)
```bash
php artisan make:migration create_document_chunks_table
```

Fill in schema as shown above

---

### Step 3: Create Model (GREEN)
```bash
php artisan make:model DocumentChunk
```

Add fillable, casts, and relationship

---

### Step 4: Update KnowledgeBase Model
Add `chunks()` relationship method

---

### Step 5: Run Migration
```bash
php artisan migrate
```

---

### Step 6: Run Tests
```bash
php artisan test --filter=DocumentChunkTest
```

All tests should pass ✅

---

### Step 7: Code Review
Check for:
- SQL injection protection (Eloquent ORM ✅)
- Mass assignment protection (fillable defined ✅)
- Cascade deletes configured ✅
- Proper indexing ✅

---

## Acceptance Criteria

- [ ] Migration runs without errors
- [ ] Can create `DocumentChunk` records
- [ ] `DocumentChunk` belongs to `KnowledgeBase`
- [ ] `KnowledgeBase` has many `DocumentChunk`
- [ ] Metadata field casts to array
- [ ] All tests pass (6/6)
- [ ] Test coverage 100%
- [ ] Code passes review

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Migration conflict | Low | Medium | Check existing migrations first |
| Missing indexes | Low | High | Include indexes in schema |
| Cascade delete issues | Low | High | Use `onDelete('cascade')` |

---

## Testing Strategy

### Unit Tests
- Model creation/retrieval
- Relationships
- Type casting
- Query scoping

### Integration Tests
- Create chunk with knowledge base
- Delete knowledge base → chunks deleted
- Query chunks by KB

---

## Performance Considerations

- **Indexes:** On `knowledge_base_id` and `qdrant_point_id` for fast lookups
- **Chunking:** Will handle large documents split into ~500 token chunks
- **Cascade Deletes:** Automatic cleanup when KB is deleted

---

## Next Steps After Completion

1. Commit with message: `feat: add document chunks migration and model (#104)`
2. Mark issue #104 as complete
3. Move to issue #105 (OpenAI Embeddings Service)

---

**Ready to implement?** Reply "yes" to proceed with TDD workflow.
