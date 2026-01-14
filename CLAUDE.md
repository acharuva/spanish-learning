# Project Instructions

## Workflow

- When the user makes a major decision or change, review the implementation plan and update it accordingly.
- Use the TodoWrite tool to track the updated plan and ensure all steps are visible.

## Deployment

- S3 Bucket: `spanish-words-433730330450`
- Website URL: http://spanish-words-433730330450.s3-website-us-east-1.amazonaws.com
- Sync command: `aws s3 sync pages/ s3://spanish-words-433730330450/ --content-type "text/html"`
